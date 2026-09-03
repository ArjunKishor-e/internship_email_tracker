import sqlite3
from internship_email_tracker.email_model import Email

def get_connection():
    connection = sqlite3.connect("tracker.db")
    return connection

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            subject TEXT,
            date TEXT,
            stage TEXT
        )
    """)

    connection.commit()
    connection.close()

def insert_email(company, subject, date, stage):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO emails (company, subject, date, stage)
        VALUES (?, ?, ?, ?)
    """, (company, subject, date, stage))

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
        email = Email(row[1], row[2], row[3], row[4])
        emails.append(email)

    return emails

if __name__ == "__main__":
    create_table()

    emails = get_all_emails()
    for email in emails:
        print(email)