GENERIC_WORDS = {
    "the", "a", "an", "at", "for", "in", "of", "to", "and", "your",
    "summer", "internship", "intern", "programme", "program",
    "application", "opportunity", "position", "role",
}   

AMBIGUOUS = object()

def match_application(email, applications):
    for application in applications:
        if application.gmail_thread_id and application.gmail_thread_id == email["thread_id"]:
            return application

    email_domain = email.get("sender_domain", "")
    if email_domain:
        domain_matches = [
            application for application in applications
            if application.company and _domain_matches_company(email_domain, application.company)
        ]
        if len(domain_matches) == 1:
            return domain_matches[0]
        elif len(domain_matches) > 1:
            return break_tie_by_role_title(email, domain_matches)
        
    return None

def break_tie_by_role_title(email, candidates):
    subject = email.get("subject", "")
    scored = [
        (candidate, role_overlap_score(subject, candidate.role_title))
        for candidate in candidates
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)

    best_candidate, best_score = scored[0]
    second_best_score = scored[1][1] if len(scored) > 1 else 0

    if best_score > 0 and best_score > second_best_score:
        return best_candidate

    return AMBIGUOUS


def role_overlap_score(subject, role_title):
    if not role_title:
        return 0

    subject_words = meaningful_words(subject)
    role_words = meaningful_words(role_title)

    return len(subject_words & role_words)


def meaningful_words(text):
    words = set(text.lower().split())
    return words - GENERIC_WORDS


def _domain_matches_company(domain, company):
    domain_root = domain.split(".")[0].lower()
    company_lower = company.lower()

    return domain_root in company_lower or company_lower in domain_root