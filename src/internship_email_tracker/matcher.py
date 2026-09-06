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

    return None


def _domain_matches_company(domain, company):
    domain_root = domain.split(".")[0].lower()
    company_lower = company.lower()

    return domain_root in company_lower or company_lower in domain_root