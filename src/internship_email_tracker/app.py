from fastapi import FastAPI, HTTPException
from internship_email_tracker.demo_data import seed_demo_data
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
DEMO_MODE = os.environ.get("DEMO_MODE", "").lower() in ("1", "true", "yes")
DB_PATH = os.environ.get("DB_PATH", "demo.db" if DEMO_MODE else "tracker.db")
db = EmailDatabase(DB_PATH)
db.create_table()

def gmail_sync_loop():
    while True:
        try:
            db.sync_gmail_to_database()
        except Exception as e:
            print (f"Gmail Sync failed: {e}")
        time.sleep(86400)

if DEMO_MODE:
    seed_demo_data(db)
else:
    threading.Thread(target=gmail_sync_loop, daemon=True).start()

@app.get("/")
def home():
     return {"status": "ok", "message": "API is running. Frontend is at http://localhost:5173"}

@app.get("/sync")
def sync():
    if DEMO_MODE:
        raise HTTPException(status_code=403, detail="Disabled in demo mode")
    return db.sync_gmail_to_database()

@app.get("/api/applications")
def api_applications():
    applications = db.get_application_timelines()
    analytics = db.get_analytics_summary()
    return {"applications": applications, "analytics": analytics, "demo_mode": DEMO_MODE}

@app.post("/rebuild")
def rebuild():
    if DEMO_MODE:
        raise HTTPException(status_code=403, detail="Disabled in demo mode")
    return db.rebuild_from_gmail()