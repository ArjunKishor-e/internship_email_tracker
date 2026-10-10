from fastapi import FastAPI
from internship_email_tracker.database import EmailDatabase
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
import os

app = FastAPI()
FRONTEND_ORIGINS = os.environ.get("FRONTEND_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = EmailDatabase(os.environ.get("DB_PATH", "tracker.db"))
db.create_table()

def gmail_sync_loop():
    while True:
        try:
            db.sync_gmail_to_database()
        except Exception as e:
            print (f"Gmail Sync failed: {e}")
        time.sleep(86400)

threading.Thread(target=gmail_sync_loop, daemon=True).start()

@app.get("/")
def home():
     return {"status": "ok", "message": "API is running. Frontend is at http://localhost:5173"}

@app.get("/sync")
def sync():
    return db.sync_gmail_to_database()

@app.get("/api/applications")
def api_applications():
    applications = db.get_application_timelines()
    analytics = db.get_analytics_summary()
    return {"applications": applications, "analytics": analytics}

@app.post("/rebuild")
def rebuild():
    return db.rebuild_from_gmail()