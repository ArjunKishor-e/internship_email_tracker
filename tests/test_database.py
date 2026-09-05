import os
from internship_email_tracker.database import create_table, insert_email, get_all_emails

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