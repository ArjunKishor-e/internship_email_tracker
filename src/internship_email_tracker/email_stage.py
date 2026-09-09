STAGE_ORDER = ["Applied", "Assessment", "Interview", "AssessmentCentre", "Offered"]


def should_update_stage(current_stage, new_stage):
    if current_stage == "Rejected":
        return False

    if new_stage == "Rejected":
        return True

    if new_stage == "Other":
        return False

    if new_stage not in STAGE_ORDER:
        return False

    if current_stage not in STAGE_ORDER:
        return True

    return STAGE_ORDER.index(new_stage) > STAGE_ORDER.index(current_stage)