import sqlite3
from internship_email_tracker.email_model import Email
from internship_email_tracker.classifier import classify_email
from internship_email_tracker.gmail_client import get_recent_emails

def get_connection():
    connection = sqlite3.connect("tracker.db")
    return connection

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmail_id TEXT UNIQUE,
            company TEXT,
            subject TEXT,
            date TEXT,
            stage TEXT
        )
    """)

    connection.commit()
    connection.close()

def insert_email(gmail_id, company, subject, date, body, stage = None):
    if stage is None:
        stage = classify_email(subject,body)
    
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails (gmail_id, company, subject, date, stage)
        VALUES (?, ?, ?, ?, ?)
    """, (gmail_id, company, subject, date, stage))

    connection.commit()
    connection.close()

def get_all_emails():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()

    connection.close()

    emails = []
    for row in rows:
        email = Email(row[2], row[3], row[4], row[5])
        emails.append(email)

    return emails
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