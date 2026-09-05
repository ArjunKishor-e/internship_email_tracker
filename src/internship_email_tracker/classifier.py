def classify_email(subject,body):
    subject_lower=subject.lower()
    body_lower= body.lower()

    if "interview" in subject_lower or "interview" in body_lower:
        return "Interview"
    elif "assessment" in subject_lower or "online assessment" in subject_lower or "coding test" in subject_lower or "technical test" in subject_lower or "assessment" in body_lower or "online assessment" in body_lower or "coding test" in body_lower or "technical test" in body_lower:
        return "Assessment"
    elif "reject" in subject_lower or "unfortunately" in subject_lower or "not progressed" in subject_lower or "unsuccessful" in subject_lower or "reject" in body_lower or "unfortunately" in body_lower or "not progressed" in body_lower or "unsuccessful" in body_lower:
        return "Rejected"
    elif "congratulations" in subject_lower or "pleased" in subject_lower or "delighted" in subject_lower or "job offer" in subject_lower or "offer of employment" in subject_lower or "congratulations" in body_lower or "pleased" in body_lower or "delighted" in body_lower or "job offer" in subject_lower or "offer of employment" in body_lower:
        return "Offered"
    else:
        return "Applied"

