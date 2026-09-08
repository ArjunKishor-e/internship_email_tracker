from internship_email_tracker.matcher import match_application


class FakeApplication:
    def __init__(self, company, gmail_thread_id=None):
        self.company = company
        self.gmail_thread_id = gmail_thread_id


def test_matches_by_thread_id():
    apps = [FakeApplication("Google", gmail_thread_id="thread123")]
    email = {"thread_id": "thread123", "sender_domain": "google.com"}

    result = match_application(email, apps)

    assert result is apps[0]


def test_matches_by_domain_when_single_candidate():
    apps = [FakeApplication("Google", gmail_thread_id="other_thread")]
    email = {"thread_id": "new_thread", "sender_domain": "google.com"}

    result = match_application(email, apps)

    assert result is apps[0]


def test_ambiguous_domain_match_returns_none():
    apps = [
        FakeApplication("Google", gmail_thread_id="thread_a"),
        FakeApplication("Google", gmail_thread_id="thread_b"),
    ]
    email = {"thread_id": "new_thread", "sender_domain": "google.com"}

    result = match_application(email, apps)

    assert result is None


def test_no_match_returns_none():
    apps = [FakeApplication("Amazon", gmail_thread_id="thread_a")]
    email = {"thread_id": "new_thread", "sender_domain": "google.com"}

    result = match_application(email, apps)

    assert result is None


def test_empty_applications_list_returns_none():
    email = {"thread_id": "new_thread", "sender_domain": "google.com"}

    result = match_application(email, [])

    assert result is None