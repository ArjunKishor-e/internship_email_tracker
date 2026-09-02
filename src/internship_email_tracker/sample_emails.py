from internship_email_tracker.email import Email
from internship_email_tracker.classifier import classify_email

sample_emails = [
    Email("Amazon", "Assessment Centre", "Sep 2", classify_email("Assessment Centre")),
    Email("Microsoft", "OA Invitation", "Oct 2", classify_email("OA Invitation")),
    Email("Google", "OA Invitation", "Aug 2", classify_email("OA Invitation")),
    Email("Meta", "Interview", "Feb 2", classify_email ("Interview")),
]