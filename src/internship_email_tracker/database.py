from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from internship_email_tracker.models import Base, EmailRecord
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
        session.rollback()  # mimics old INSERT OR IGNORE behaviour
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


def sync_gmail_to_database():
    emails = get_recent_emails(10)

    for email in emails:
        insert_email(email["id"], email["company"], email["subject"], email["date"], email["body"])

    print("Gmail sync complete")


if __name__ == "__main__":
    create_table()
    sync_gmail_to_database()

    emails = get_all_emails()
    for email in emails:
        print(email)