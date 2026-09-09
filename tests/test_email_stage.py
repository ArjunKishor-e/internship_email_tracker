from internship_email_tracker.email_stage import should_update_stage


def test_forward_progression_is_allowed():
    assert should_update_stage("Applied", "Assessment") is True

def test_backward_progression_is_blocked():
    assert should_update_stage("Interview", "Applied") is False

def test_same_stage_is_not_an_update():
    assert should_update_stage("Assessment", "Assessment") is False

def test_rejected_always_wins():
    assert should_update_stage("Interview", "Rejected") is True
    assert should_update_stage("Applied", "Rejected") is True

def test_nothing_changes_after_rejected():
    assert should_update_stage("Rejected", "Interview") is False
    assert should_update_stage("Rejected", "Offered") is False

def test_other_never_updates_stage():
    assert should_update_stage("Applied", "Other") is False
    assert should_update_stage("Interview", "Other") is False

def test_assessment_centre_progresses_correctly():
    assert should_update_stage("Interview", "AssessmentCentre") is True
    assert should_update_stage("AssessmentCentre", "Offered") is True
    assert should_update_stage("AssessmentCentre", "Interview") is False