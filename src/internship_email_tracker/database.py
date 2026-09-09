from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from internship_email_tracker.email_stage import should_update_stage, STAGE_ORDER
from internship_email_tracker.matcher import match_application
from internship_email_tracker.models import Base, EmailRecord, Application, StatusHistory
from internship_email_tracker.email_model import Email
from internship_email_tracker.classifier import classify_email
from internship_email_tracker.gmail_client import get_recent_emails
from internship_email_tracker.analytics import conversion_rate, average_days_between_stages, build_application_timelines

class EmailDatabase:
        
    def __init__ (self,db_name="tracker.db"):
        self.db_name = db_name
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.Session =sessionmaker(bind=self.engine)

    def create_table(self):
        Base.metadata.create_all(self.engine)   


    def insert_email(self, gmail_id, company, subject, date, body, stage=None):
        if stage is None:
            stage = classify_email(subject, body)

        session = self.Session()
        try:
            record = EmailRecord(
                gmail_id=gmail_id,
                company=company,
                subject=subject,
                date=date,
                stage=stage,
            )
            session.add(record)
            session.commit()
        except IntegrityError:
            session.rollback() 
        finally:
            session.close()


    def get_all_emails(self):
        session = self.Session()
        records = session.query(EmailRecord).all()
        session.close()

        return [Email(r.company, r.subject, r.date, r.stage) for r in records]

    def insert_email_with_application(self, email):
        stage = classify_email(email["subject"], email["body"])

        session = self.Session()
        try:
            existing_applications = session.query(Application).all()
            matched_application = match_application(email, existing_applications)

            if matched_application is None:
                matched_application = Application(
                    company=email["company"],
                    gmail_thread_id=email["thread_id"],
                    current_stage=stage,
                )
                session.add(matched_application)
                session.flush()

            record = EmailRecord(
                gmail_id=email["id"],
                application_id=matched_application.id,
                company=email["company"],
                subject=email["subject"],
                date=email["date"],
                stage=stage,
            )
            session.add(record)
            session.flush()

            if should_update_stage(matched_application.current_stage, stage):
                matched_application.current_stage = stage
                session.add(StatusHistory(
                    application_id=matched_application.id,
                    stage=stage,
                    source_email_id=record.id,
                ))
            session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            session.close()

    def get_analytics_summary(self):
            session = self.Session()
            applications = session.query(Application).all()
            status_entries = session.query(StatusHistory).all()
            session.close()

            total = len(applications)

            summary = {
            "total_applications": total,
            "conversion_rates": {},
            "average_days": {},
            }

            for stage in STAGE_ORDER:
                summary["conversion_rates"][stage] = conversion_rate(total, status_entries, stage)

            stage_pairs = list(zip(STAGE_ORDER, STAGE_ORDER[1:]))
            for from_stage, to_stage in stage_pairs:
                key = f"{from_stage}_to_{to_stage}"
                summary["average_days"][key] = average_days_between_stages(status_entries, from_stage, to_stage)

            return summary        

    def get_application_timelines(self):
        session = self.Session()
        applications = session.query(Application).all()
        status_entries = session.query(StatusHistory).all()
        session.close()

        return build_application_timelines(applications, status_entries)
    
    def sync_gmail_to_database(self):
        emails = get_recent_emails(10)

        for email in emails:
            self.insert_email_with_application(email)

        print("Gmail sync complete")

    def close(self):
        self.engine.dispose()


if __name__ == "__main__":
    db = EmailDatabase()
    db.create_table()
    db.sync_gmail_to_database()

    for email in  db.get_all_emails():
        print(email)