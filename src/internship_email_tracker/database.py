from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from internship_email_tracker.matcher import match_application
from internship_email_tracker.models import Base, EmailRecord, Application
from internship_email_tracker.email_model import Email
from internship_email_tracker.classifier import classify_email
from internship_email_tracker.gmail_client import get_recent_emails

class EmailDatabase:
        
    def __init__ (self,db_name="tracker.db"):
        self.db_name = db_name
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.Session =sessionmaker(bind=self.engine)

    def create_table(self):
        Base.metadata.create_all(self.engine)   


    def insert_email(self, gmail_id, company, subject, date, body, stage=None, db_name="tracker.db"):
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
            session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            session.close()


    def sync_gmail_to_database(db_name="tracker.db"):
        emails = get_recent_emails(10)

        for email in emails:
            self.insert_email_with_application(email)

        print("Gmail sync complete")


    if __name__ == "__main__":
        db = EmailDatabase()
        db.create_table()
        db.sync_gmail_to_database()

        for email in  db.get_all_emails():
            print(email)