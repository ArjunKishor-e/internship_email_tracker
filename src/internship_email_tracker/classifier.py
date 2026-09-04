def classify_email(subject):
    subject_lower=subject.lower()

    if "interview" in subject_lower:
        return "Interview"
    elif "assessment" in subject_lower or "online assessment" in subject_lower or "coding test" in subject_lower or "technical test" in subject_lower:
        return "Assessment"
    elif "reject" in subject_lower or "unfortunately" in subject_lower or "not progressed" in subject_lower or "unsuccessful" in subject_lower:
        return "Rejected"
    elif "congratulations" in subject_lower or "pleased" in subject_lower or "delighted" in subject_lower or "job offer" in subject_lower or "offer of employment" in subject_lower:
        return "Offered"
    else:
        return "Applied"