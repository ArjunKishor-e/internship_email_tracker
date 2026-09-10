from internship_email_tracker.email_stage import STAGE_ORDER


def applications_that_reached(status_entries, stage):
    if stage not in STAGE_ORDER:
        raise ValueError(f"Unknown stage: {stage}")

    target_index = STAGE_ORDER.index(stage)
    reached = set()

    for entry in status_entries:
        if entry.stage in STAGE_ORDER and STAGE_ORDER.index(entry.stage) >= target_index:
            reached.add(entry.application_id)

    return reached


def conversion_rate(total_applications, status_entries, stage):
    if total_applications == 0:
        return 0.0

    reached = applications_that_reached(status_entries, stage)
    return len(reached) / total_applications


def average_days_between_stages(status_entries, from_stage, to_stage):
    from_times = {}
    to_times = {}

    for entry in status_entries:
        if entry.stage == from_stage:
            if entry.application_id not in from_times or entry.changed_at < from_times[entry.application_id]:
                from_times[entry.application_id] = entry.changed_at
        if entry.stage == to_stage:
            if entry.application_id not in to_times or entry.changed_at < to_times[entry.application_id]:
                to_times[entry.application_id] = entry.changed_at

    diffs = []
    for app_id, from_time in from_times.items():
        if app_id in to_times:
            diff_days = (to_times[app_id] - from_time).total_seconds() / 86400
            if diff_days >= 0:
                diffs.append(diff_days)

    if not diffs:
        return None

    return sum(diffs) / len(diffs)

def build_application_timelines(applications, status_entries):
    entries_by_application = {}
    for entry in status_entries:
        entries_by_application.setdefault(entry.application_id, []).append(entry)

    timelines = []

    for application in applications:
        app_entries = entries_by_application.get(application.id, [])
        app_entries.sort(key=lambda e: e.changed_at)

        history = []
        previous_time = None

        for entry in app_entries:
            days_since_previous = None
            if previous_time is not None:
                days_since_previous = (entry.changed_at - previous_time).total_seconds() / 86400

            history.append({
                "stage": entry.stage,
                "date": entry.changed_at,
                "days_since_previous": days_since_previous,
            })
            previous_time = entry.changed_at

        timelines.append({
            "company": application.company,
            "role_title": application.role_title,
            "current_stage": application.current_stage,
            "history": history,
            "gmail_thread_id": application.gmail_thread_id,
        })

    return timelines