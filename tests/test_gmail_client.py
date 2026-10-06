from internship_email_tracker.gmail_client import parse_message


def test_no_sender_name_fallback():
    msg = {
        "id": "msg123",
        "threadId": "thread123",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Deloitte Online Assessment Feedback Report"},
                {"name": "Date", "value": "Mon, 1 Jan 2026 00:00:00 +0000"},
                {"name": "From", "value": "deloitteearlycareers@email.cappassessments.com"},
            ],
        },
    }

    result = parse_message(msg)

    assert "deloitte" not in result["company"].lower()