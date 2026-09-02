from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from internship_email_tracker.sample_emails import sample_emails
from internship_email_tracker.classifier import classify_email

app = FastAPI()

templates = Jinja2Templates(directory="src/internship_email_tracker/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"emails": sample_emails})