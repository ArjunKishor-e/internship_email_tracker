from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="src/internship_email_tracker/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})