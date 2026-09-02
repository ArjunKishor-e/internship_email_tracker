from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from internship_email_tracker.sample_emails import sample_emails
from internship_email_tracker.classifier import classify_email

app = FastAPI()

templates = Jinja2Templates(directory="src/internship_email_tracker/templates")

@app.get("/")
def home(request: Request):
    applied_count = sum(1 for email in sample_emails if email.stage == "Applied")
    assessment_count = sum(1 for email in sample_emails if email.stage == "Assessment")
    interview_count = sum(1 for email in sample_emails if email.stage == "Interview")
    rejected_count = sum(1 for email in sample_emails if email.stage == "Rejected")
    offer_count = sum(1 for email in sample_emails if email.stage == "Offer")

    return templates.TemplateResponse(request, "index.html", {
        "emails": sample_emails,
        "applied_count": applied_count,
        "assessment_count": assessment_count,
        "interview_count": interview_count,
        "rejected_count": rejected_count,
        "offer_count": offer_count,
    })