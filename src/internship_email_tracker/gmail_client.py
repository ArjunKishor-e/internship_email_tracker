from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
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

def get_recent_emails(max_results=10, query="interview OR application OR assessment OR offer OR rejected"):
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me", maxResults=max_results, q=query
    ).execute()

    messages = results.get("messages", [])

    fetched_emails = []

    def handle_response(request_id, response, exception):
        if exception is None:
            fetched_emails.append(parse_message(response))

    batch = service.new_batch_http_request(callback=handle_response)
    for message in messages:
        batch.add(service.users().messages().get(userId="me", id=message["id"]))

    batch.execute()

    return fetched_emails

def parse_message(msg):
    headers = msg["payload"]["headers"]
    body = get_email_body(msg["payload"])

    subject = ""
    date = ""
    company = ""
    sender_domain = ""

    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]
        if header["name"] == "Date":
            date = header["value"]
        if header["name"] == "From":
            raw_sender = header["value"]
            name, email_address = parseaddr(raw_sender)
            if name:
                company = name
            else:
                company = email_address
            if "@" in email_address:
                sender_domain = email_address.split("@")[1]

    return {
        "id": msg["id"],
        "subject": subject,
        "date": date,
        "company": company,
        "body": body,
        "sender_domain": sender_domain,
        "thread_id": msg.get("threadId", ""),
    }


if __name__ == "__main__":
    emails = get_recent_emails(5)
    for email in emails:
        print(email)
