def classify_email(subject):
    subject_lower=subject.lower()

    if "interview" in subject_lower:
        return "Interview"
    elif "assessment" in subject_lower or "oa" in subject_lower:
        return "Assessment"
    elif "reject" in subject_lower or "unfortunately" in subject_lower:
        return "Rejected"
    elif "congratulations" in subject_lower or "pleased" in subject_lower or "delighted" in subject_lower:
        return "Offered"
    else:
        return "Applied"
    