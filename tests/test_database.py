import os
from internship_email_tracker.database import create_table, insert_email, get_all_emails
from internship_email_tracker.database import insert_email_with_application
from internship_email_tracker.models import Application
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB = "test_tracker.db"

def setup_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    create_table(TEST_DB)

def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_insert_and_retrieve_email():
    insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "", db_name=TEST_DB)

    emails = get_all_emails(TEST_DB)

    assert len(emails) == 1
    assert emails[0].company == "Amazon"
    assert emails[0].stage == "Interview"

def test_duplicate_gmail_id_is_ignored():
    insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "", db_name=TEST_DB)
    insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "", db_name=TEST_DB)

    emails = get_all_emails(TEST_DB)

    assert len(emails) == 1

def test_different_gmail_ids_are_both_stored():
    insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "", db_name=TEST_DB)
    insert_email("gmail456", "Google", "Assessment invitation", "Sep 3", "", db_name=TEST_DB)

    emails = get_all_emails(TEST_DB)

    assert len(emails) == 2

def test_new_application_created_when_no_match():
    email = {
        "id": "gmail1",
        "thread_id": "thread1",
        "sender_domain": "google.com",
        "company": "Google",
        "subject": "Interview invitation",
        "date": "Sep 2",
        "body": "",
    }

    insert_email_with_application(email, db_name=TEST_DB)

    engine = create_engine(f"sqlite:///{TEST_DB}")
    Session = sessionmaker(bind=engine)
    session = Session()
    applications = session.query(Application).all()
    session.close()
    engine.dispose()

    assert len(applications) == 1
    assert applications[0].company == "Google"
    assert applications[0].gmail_thread_id == "thread1"


def test_existing_application_reused_on_thread_match():
    first_email = {
        "id": "gmail1",
        "thread_id": "thread1",
        "sender_domain": "google.com",
        "company": "Google",
        "subject": "Application received",
        "date": "Sep 1",
        "body": "",
    }
    second_email = {
        "id": "gmail2",
        "thread_id": "thread1",
        "sender_domain": "google.com",
        "company": "Google",
        "subject": "Interview invitation",
        "date": "Sep 2",
        "body": "",
    }

    insert_email_with_application(first_email, db_name=TEST_DB)
    insert_email_with_application(second_email, db_name=TEST_DB)

    engine = create_engine(f"sqlite:///{TEST_DB}")
    Session = sessionmaker(bind=engine)
    session = Session()
    applications = session.query(Application).all()
    session.close()
    engine.dispose()

    assert len(applications) == 1


def test_email_linked_to_correct_application():
    email = {
        "id": "gmail1",
        "thread_id": "thread1",
        "sender_domain": "google.com",
        "company": "Google",
        "subject": "Interview invitation",
        "date": "Sep 2",
        "body": "",
    }

    insert_email_with_application(email, db_name=TEST_DB)

    emails = get_all_emails(TEST_DB)
    assert len(emails) == 1

    engine = create_engine(f"sqlite:///{TEST_DB}")
    Session = sessionmaker(bind=engine)
    session = Session()
    from internship_email_tracker.models import EmailRecord
    record = session.query(EmailRecord).first()
    application = session.query(Application).first()
    session.close()
    engine.dispose()

    assert record.application_id == application.id