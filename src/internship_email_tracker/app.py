from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from internship_email_tracker.database import get_all_emails, sync_gmail_to_database, create_table
from internship_email_tracker.classifier import classify_email


app = FastAPI()
create_table()

templates = Jinja2Templates(directory="src/internship_email_tracker/templates")

@app.get("/")
def home(request: Request):
    emails = get_all_emails()

    applied_count = sum(1 for email in emails if email.stage == "Applied")
    assessment_count = sum(1 for email in emails if email.stage == "Assessment")
    interview_count = sum(1 for email in emails if email.stage == "Interview")
    rejected_count = sum(1 for email in emails if email.stage == "Rejected")
    offer_count = sum(1 for email in emails if email.stage == "Offer")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "emails": emails,
            "applied_count": applied_count,
            "assessment_count": assessment_count,
            "interview_count": interview_count,
            "rejected_count": rejected_count,
            "offer_count": offer_count,
        }
    )
@app.get("/sync")
def sync(request: Request):
    sync_gmail_to_database()
    return RedirectResponse(url="/", status_code=303)