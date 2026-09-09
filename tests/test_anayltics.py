from datetime import datetime, timedelta, timezone
from internship_email_tracker.analytics import (
    applications_that_reached,
    conversion_rate,
    average_days_between_stages,
    build_application_timelines,
)


class FakeStatusEntry:
    def __init__(self, application_id, stage, changed_at):
        self.application_id = application_id
        self.stage = stage
        self.changed_at = changed_at


def test_applications_that_reached_includes_later_stages():
    entries = [
        FakeStatusEntry(1, "Applied", datetime.now(timezone.utc)),
        FakeStatusEntry(2, "Interview", datetime.now(timezone.utc)),
    ]

    reached = applications_that_reached(entries, "Assessment")

    assert reached == {2}

def test_applications_that_reached_excludes_earlier_stages():
    entries = [FakeStatusEntry(1, "Applied", datetime.now(timezone.utc))]

    reached = applications_that_reached(entries, "Interview")

    assert reached == set()

def test_conversion_rate_basic():
    entries = [
        FakeStatusEntry(1, "Interview", datetime.now(timezone.utc)),
        FakeStatusEntry(2, "Applied", datetime.now(timezone.utc)),
    ]

    rate = conversion_rate(total_applications=2, status_entries=entries, stage="Interview")

    assert rate == 0.5

def test_conversion_rate_zero_applications():
    rate = conversion_rate(total_applications=0, status_entries=[], stage="Interview")

    assert rate == 0.0

def test_average_days_between_stages():
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    entries = [
        FakeStatusEntry(1, "Applied", base),
        FakeStatusEntry(1, "Interview", base + timedelta(days=5)),
        FakeStatusEntry(2, "Applied", base),
        FakeStatusEntry(2, "Interview", base + timedelta(days=10)),
    ]

    avg = average_days_between_stages(entries, "Applied", "Interview")

    assert avg == 7.5

def test_average_days_between_stages_no_qualifying_applications():
    entries = [FakeStatusEntry(1, "Applied", datetime.now(timezone.utc))]

    avg = average_days_between_stages(entries, "Applied", "Interview")

    assert avg is None

class FakeApplication:
    def __init__(self, id, company, role_title, current_stage):
        self.id = id
        self.company = company
        self.role_title = role_title
        self.current_stage = current_stage


def test_build_application_timelines_basic():
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    applications = [FakeApplication(1, "Google", "Software Engineer", "Interview")]
    entries = [
        FakeStatusEntry(1, "Applied", base),
        FakeStatusEntry(1, "Assessment", base + timedelta(days=3)),
        FakeStatusEntry(1, "Interview", base + timedelta(days=8)),
    ]

    timelines = build_application_timelines(applications, entries)

    assert len(timelines) == 1
    assert timelines[0]["company"] == "Google"
    assert timelines[0]["current_stage"] == "Interview"
    assert timelines[0]["history"][0]["days_since_previous"] is None
    assert timelines[0]["history"][1]["days_since_previous"] == 3.0
    assert timelines[0]["history"][2]["days_since_previous"] == 5.0

def test_build_application_timelines_no_history():
    applications = [FakeApplication(1, "Amazon", None, "Applied")]

    timelines = build_application_timelines(applications, [])

    assert timelines[0]["history"] == []