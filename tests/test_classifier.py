from internship_email_tracker.classifier import classify_email

def test_interview_keyword_in_subject():
    result = classify_email("Interview invitation", "")
    assert result == "Interview"

def test_assessment_keyword_in_subject():
    result = classify_email("Online assessment invitation", "")
    assert result == "Assessment"

def test_rejected_keyword_in_subject():
    result = classify_email("Unfortunately, we will not be proceeding", "")
    assert result == "Rejected"

def test_offer_keyword_in_subject():
    result = classify_email("Congratulations! Job offer", "")
    assert result == "Offered"

def test_unrelated_email_returns_other():
    result = classify_email("Your Google Account data was shared", "")
    assert result == "Other"

def test_keyword_found_only_in_body():
    result = classify_email("Update regarding your application", "We would like to schedule an interview with you.")
    assert result == "Interview"