from googleapiclient.discovery import build
from internship_email_tracker.gmail_auth import get_gmail_credentials
from email.utils import parseaddr
import base64

def get_email_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")

    if payload.get("mimeType") == "text/plain":
        data = payload["body"].get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8")

    return ""

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

        body = get_email_body(msg["payload"])
        print(body)

        subject = ""
        date = ""
        company = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]
            if header["name"] == "Date":
                date = header["value"]
            if header["name"] == "From":
                raw_sender = header["value"]
                name, email_address = parseaddr(raw_sender)
                if name:
                    company=name
                else:
                    company=email_address

        emails.append({"id": message ["id"], "subject": subject, "date": date, "company": company, "body":body})

    return emails


if __name__ == "__main__":
    emails = get_recent_emails(5)
    for email in emails:
        print(email)
