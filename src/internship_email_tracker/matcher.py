import re

GENERIC_WORDS = {
    "the", "a", "an", "at", "for", "in", "of", "to", "and", "your",
    "summer", "internship", "intern", "programme", "program",
    "application", "opportunity", "position", "role",
}
 
AMBIGUOUS = "AMBIGUOUS"

PLATFORM_DOMAINS = {
    "myworkday", "workday", "lever", "greenhouse", "icims", "smartrecruiters",
    "aon-assessment", "cappassessments", "arcticshores", "hirevue", "successfactors",
}

COMPANY_STOPWORDS = {
    "uk", "the", "and", "team", "hiring", "recruiting", "recruitment",
    "careers", "group", "ltd", "limited", "plc", "llp", "talent", "jobs",
}
 
def match_application(email, applications):
    for application in applications:
        if application.gmail_thread_id and application.gmail_thread_id == email["thread_id"]:
            return application
 
    email_domain = email.get("sender_domain", "")
    if email_domain and domain_root(email_domain) not in PLATFORM_DOMAINS:
        domain_matches = [
            application for application in applications
            if application.company and _domain_matches_company(email_domain, application.company)
        ]
        if len(domain_matches) == 1:
            return domain_matches[0]
        if len(domain_matches) > 1:
            return _break_tie_by_role_title(email, domain_matches)
 
    email_company = email.get("company", "")
    if email_company:
        company_matches = [
            application for application in applications
            if application.company and _company_names_match(email_company, application.company)
        ]
        if len(company_matches) == 1:
            return company_matches[0]
        if len(company_matches) > 1:
            return _break_tie_by_role_title(email, company_matches)
        
    subject = email.get("subject", "")
    if subject:
        subject_matches = [
            application for application in applications
            if application.company and _subject_mentions_company(subject, application.company)
        ]
        if len(subject_matches) == 1:
            return subject_matches[0]
        if len(subject_matches) > 1:
            return _break_tie_by_role_title(email, subject_matches)
 
    return None
 
 
def _break_tie_by_role_title(email, candidates):
    subject = email.get("subject", "")
    scored = [
        (candidate, _role_overlap_score(subject, candidate.role_title))
        for candidate in candidates
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
 
    best_candidate, best_score = scored[0]
    second_best_score = scored[1][1] if len(scored) > 1 else 0
 
    if best_score > 0 and best_score > second_best_score:
        return best_candidate
 
    return AMBIGUOUS
 
 
def _role_overlap_score(subject, role_title):
    if not role_title:
        return 0
 
    subject_words = _meaningful_words(subject)
    role_words = _meaningful_words(role_title)
 
    return len(subject_words & role_words)
 
 
def _meaningful_words(text):
    words = set(text.lower().split())
    return words - GENERIC_WORDS
 
 
def domain_root(domain):
    labels = domain.lower().split(".")
    if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in {"co", "com", "org", "ac", "gov"}:
        return labels[-3]
    if len(labels) >= 2:
        return labels[-2]
    return labels[0]


def _domain_matches_company(domain, company):
    root = domain_root(domain)
    company_lower = company.lower()

    return root in company_lower or company_lower in root
 
 
def _company_names_match(company_a, company_b):
    a_lower = company_a.lower()
    b_lower = company_b.lower()
 
    return a_lower in b_lower or b_lower in a_lower

def _company_key_words(company):
    words = re.findall(r"[a-z0-9]+", company.lower())
    return {word for word in words if len(word) >= 3 and word not in COMPANY_STOPWORDS}


def _subject_mentions_company(subject, company):
    key_words = _company_key_words(company)
    if not key_words:
        return False
    subject_words = set(re.findall(r"[a-z0-9]+", subject.lower()))
    return key_words <= subject_words