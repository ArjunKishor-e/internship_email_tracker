from googleapiclient.discovery import build
from internship_email_tracker.gmail_auth import get_gmail_credentials

def get_recent_emails(max_results=10):
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []
    for message in messages:
        msg = service.users().messages().get(
            userId="me", id=message["id"]
        ).execute()

        headers = msg["payload"]["headers"]
        subject = ""
        date = ""
        company = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]
            if header["name"] == "Date":
                date = header["value"]
            if header["name"] == "From":
                company = header["value"]

        emails.append({"id": message ["id"], "subject": subject, "date": date, "sender": company})

    return emails


if __name__ == "__main__":
    emails = get_recent_emails(5)
    for email in emails:
        print(email)