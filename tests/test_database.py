import os
from internship_email_tracker.database import EmailDatabase
from internship_email_tracker.models import Application, EmailRecord

TEST_DB = "test_tracker.db"

def setup_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_insert_and_retrieve_email():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    db.insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "")

    emails = db.get_all_emails()

    assert len(emails) == 1
    assert emails[0].company == "Amazon"
    assert emails[0].stage == "Interview"

    db.close()

def test_duplicate_gmail_id_is_ignored():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    db.insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "")
    db.insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "")

    emails = db.get_all_emails()

    assert len(emails) == 1

    db.close()

def test_different_gmail_ids_are_both_stored():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    db.insert_email("gmail123", "Amazon", "Interview invitation", "Sep 2", "")
    db.insert_email("gmail456", "Google", "Assessment invitation", "Sep 3", "")

    emails = db.get_all_emails()

    assert len(emails) == 2

    db.close()

def test_new_application_created_when_no_match():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    email = {
        "id": "gmail1",
        "thread_id": "thread1",
        "sender_domain": "google.com",
        "company": "Google",
        "subject": "Interview invitation",
        "date": "Sep 2",
        "body": "",
    }

    db.insert_email_with_application(email)

    session = db.Session()
    applications = session.query(Application).all()
    session.close()

    assert len(applications) == 1
    assert applications[0].company == "Google"
    assert applications[0].gmail_thread_id == "thread1"

    db.close()

def test_existing_application_reused_on_thread_match():
    db = EmailDatabase(TEST_DB)
    db.create_table()
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

    db.insert_email_with_application(first_email)
    db.insert_email_with_application(second_email)

    session = db.Session()
    applications = session.query(Application).all()
    session.close()

    assert len(applications) == 1

    db.close()

def test_email_linked_to_correct_application():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    email = {
        "id": "gmail1",
        "thread_id": "thread1",
        "sender_domain": "google.com",
        "company": "Google",
        "subject": "Interview invitation",
        "date": "Sep 2",
        "body": "",
    }

    db.insert_email_with_application(email)

    emails = db.get_all_emails()
    assert len(emails) == 1

    session = db.Session()
    record = session.query(EmailRecord).first()
    application = session.query(Application).first()
    session.close()

    assert record.application_id == application.id

    db.close()