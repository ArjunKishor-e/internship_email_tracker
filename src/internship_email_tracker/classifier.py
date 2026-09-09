def classify_email(subject, body):
    subject_lower = subject.lower()
    body_lower = body.lower()

    if (
        "your interview" in subject_lower
        or "interview invitation" in subject_lower
        or "interview scheduled" in subject_lower
        or "invite you to interview" in subject_lower
        or "schedule your interview" in subject_lower
        or "your interview" in body_lower
        or "interview invitation" in body_lower
        or "interview scheduled" in body_lower
        or "invite you to interview" in body_lower
        or "schedule your interview" in body_lower
        or "schedule an interview" in body_lower
    ):
        return "Interview"
    elif (
        "assessment centre" in subject_lower
        or "assessment center" in subject_lower
        or "assessment day" in subject_lower
        or "final round" in subject_lower
        or "assessment centre" in body_lower
        or "assessment center" in body_lower
        or "assessment day" in body_lower
        or "final round" in body_lower
    ):
        return "AssessmentCentre"
    elif (
        "online assessment" in subject_lower
        or "coding test" in subject_lower
        or "technical test" in subject_lower
        or "complete your assessment" in subject_lower
        or "online assessment" in body_lower
        or "coding test" in body_lower
        or "technical test" in body_lower
        or "complete your assessment" in body_lower
    ):
        return "Assessment"
    elif (
        "unfortunately" in subject_lower
        or "not progressed" in subject_lower
        or "unsuccessful" in subject_lower
        or "regret to inform" in subject_lower
        or "unfortunately" in body_lower
        or "not progressed" in body_lower
        or "unsuccessful" in body_lower
        or "regret to inform" in body_lower
    ):
        return "Rejected"
    elif (
        "job offer" in subject_lower
        or "offer of employment" in subject_lower
        or "pleased to offer" in subject_lower
        or "delighted to offer" in subject_lower
        or "job offer" in body_lower
        or "offer of employment" in body_lower
        or "pleased to offer" in body_lower
        or "delighted to offer" in body_lower
    ):
        return "Offered"
    elif (
        "application" in subject_lower
        or "application" in body_lower
        or "applying" in subject_lower
        or "applying" in body_lower
        or "candidate" in subject_lower
        or "candidate" in body_lower
        or "recruitment" in subject_lower
        or "recruitment" in body_lower
        or "internship" in subject_lower
        or "internship" in body_lower
    ):
        return "Applied"
    else:
        return "Other"