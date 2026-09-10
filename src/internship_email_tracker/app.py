from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from internship_email_tracker.database import EmailDatabase
from internship_email_tracker.classifier import classify_email
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
db = EmailDatabase()
db.create_table()

async def gmail_sync_time():
    while True:
        db.sync_gmail_to_database()
        await asyncio.sleep(86400)

@app.on_event("startup")
async def start_background_sync():
    asyncio.create_task(gmail_sync_time())

templates = Jinja2Templates(directory="src/internship_email_tracker/templates")

@app.get("/")
def home(request: Request):
    emails = db.get_all_emails()
    applications = db.get_application_timelines()
    analytics = db.get_analytics_summary()
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
            "applications": applications,
            "analytics": analytics,
        }
    )
@app.get("/sync")
def sync(request: Request):
    db.sync_gmail_to_database()
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/applications")
def api_applications():
    applications = db.get_application_timelines()
    analytics = db.get_analytics_summary()
    return {"applications": applications, "analytics": analytics}