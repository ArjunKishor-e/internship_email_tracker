def classify_email(subject):
    subject_lower=subject.lower()

    if "interview" in subject_lower:
        return "Interview"
    elif "assessment" in subject_lower or "oa" in subject_lower:
        return "Assessment"
    elif "reject" in subject_lower or "unfortunately" in subject_lower:
        return "Rejected"
    else:
        return "Applied"
    
if __name__ == "__main__":
    print(classify_email("Interview invitation"))
    print(classify_email("Online assessment invitation"))
    print(classify_email("Unfortunately, we will not be proceeding"))
    print(classify_email("Application received"))