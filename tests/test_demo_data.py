import os
from internship_email_tracker.database import EmailDatabase
from internship_email_tracker.models import Application
from internship_email_tracker.demo_data import seed_demo_data

TEST_DB = "test_demo.db"


def setup_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def load_stages():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    seed_demo_data(db)
    session = db.Session()
    stages = {a.company: a.current_stage for a in session.query(Application).all()}
    session.close()
    db.close()
    return stages


def test_demo_data_produces_expected_stages():
    assert load_stages() == {
        "Northwind Labs": "Offered",
        "Brightwave Systems": "Rejected",
        "Helix Robotics": "AssessmentCentre",
        "Ardent Bank": "Applied",
        "Kestrel Aerospace": "Interview",
        "Orbit Payments": "Rejected",
        "Delta Logistics": "Assessment",
        "Cedar Health": "Applied",
    }


def test_seeding_twice_does_not_duplicate():
    db = EmailDatabase(TEST_DB)
    db.create_table()
    seed_demo_data(db)
    seed_demo_data(db)
    session = db.Session()
    count = session.query(Application).count()
    session.close()
    db.close()
    assert count == 8