from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from internship_email_tracker.matcher import match_application
from internship_email_tracker.models import Base, EmailRecord, Application
from internship_email_tracker.email_model import Email
from internship_email_tracker.classifier import classify_email
from internship_email_tracker.gmail_client import get_recent_emails


def get_engine(db_name="tracker.db"):
    return create_engine(f"sqlite:///{db_name}")


def create_table(db_name="tracker.db"):
    engine = get_engine(db_name)
    Base.metadata.create_all(engine)
    engine.dispose()


def insert_email(gmail_id, company, subject, date, body, stage=None, db_name="tracker.db"):
    if stage is None:
        stage = classify_email(subject, body)

    engine = get_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()
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
        engine.dispose()


def get_all_emails(db_name="tracker.db"):
    engine = get_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    records = session.query(EmailRecord).all()

    session.close()
    engine.dispose()

    return [Email(r.company, r.subject, r.date, r.stage) for r in records]

def insert_email_with_application(email, db_name="tracker.db"):
    stage = classify_email(email["subject"], email["body"])

    engine = get_engine(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

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
        engine.dispose()


def sync_gmail_to_database(db_name="tracker.db"):
    emails = get_recent_emails(10)

    for email in emails:
        insert_email_with_application(email, db_name=db_name)

    print("Gmail sync complete")


if __name__ == "__main__":
    create_table()
    sync_gmail_to_database()

    emails = get_all_emails()
    for email in emails:
        print(email)