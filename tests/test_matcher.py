from internship_email_tracker.matcher import match_application, AMBIGUOUS


class FakeApplication:
    def __init__(self, company, gmail_thread_id=None, role_title=None):
        self.company = company
        self.gmail_thread_id = gmail_thread_id
        self.role_title = role_title


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

    assert result == AMBIGUOUS

def test_match_application_ambiguous_domain_returns_ambiguous():
    fake_google_swe = FakeApplication(gmail_thread_id="thread_1", company="Google Software Engineering")
    fake_google_ds = FakeApplication(gmail_thread_id="thread_2", company="Google Data Science")

    new_email = {
        "thread_id": "thread_3",
        "sender_domain": "google.com",
    }

    result = match_application(new_email, [fake_google_swe, fake_google_ds])

    assert result == AMBIGUOUS


def test_no_match_returns_none():
    apps = [FakeApplication("Amazon", gmail_thread_id="thread_a")]
    email = {"thread_id": "new_thread", "sender_domain": "google.com"}

    result = match_application(email, apps)

    assert result is None


def test_empty_applications_list_returns_none():
    email = {"thread_id": "new_thread", "sender_domain": "google.com"}

    result = match_application(email, [])

    assert result is None

def test_role_title_breaks_domain_tie():
    apps = [
        FakeApplication("Google", gmail_thread_id="thread_a", role_title="Software Engineering Internship"),
        FakeApplication("Google", gmail_thread_id="thread_b", role_title="Data Science Internship"),
    ]
    email = {
        "thread_id": "new_thread",
        "sender_domain": "google.com",
        "subject": "Your Software Engineering application has been received",
    }

    result = match_application(email, apps)

    assert result is apps[0]