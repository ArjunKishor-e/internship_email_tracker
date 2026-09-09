from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from internship_email_tracker.database import EmailDatabase
from internship_email_tracker.classifier import classify_email
import asyncio

app = FastAPI()
db = EmailDatabase()
db.create_table()

async def sync_every_5_minutes():
    while True:
        db.sync_gmail_to_database()
        await asyncio.sleep(300)

@app.on_event("startup")
async def start_background_sync():
    asyncio.create_task(sync_every_5_minutes())

templates = Jinja2Templates(directory="src/internship_email_tracker/templates")

@app.get("/")
def home(request: Request):
    emails = db.get_all_emails()

    applied_count = sum(1 for email in emails if email.stage == "Applied")
    assessment_count = sum(1 for email in emails if email.stage == "Assessment")
    interview_count = sum(1 for email in emails if email.stage == "Interview")
    rejected_count = sum(1 for email in emails if email.stage == "Rejected")
    offer_count = sum(1 for email in emails if email.stage == "Offered")
    other_count = sum(1 for email in emails if email.stage == "Other")

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
            "other_count": other_count,
        }
    )
@app.get("/sync")
def sync(request: Request):
    db.sync_gmail_to_database()
    return RedirectResponse(url="/", status_code=303)