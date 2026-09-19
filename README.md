# Internship Email Tracker

Internship Tracker that Connects to Gmail, reads internship-related emails, and works out which application each one belongs to and what stage it's at (Applied, Assessment, Interview, Assessment Centre, Offered, Rejected) and displays the results in a clean table.

Applications are the core entity, each with a full stage history. Matching an email to the right application uses the Gmail thread ID first, then sender domain and refuses to update a stage if ambiguous.

## Tech stack

Python, FastAPI, SQLAlchemy (SQLite), pytest · React (Vite) · Gmail API + OAuth · Docker

## Running it

```bash
docker compose up --build
```

- Backend/API: http://localhost:8000
- Frontend: http://localhost:5173

Requires your own Gmail API credentials, since it reads a real inbox.

Without Docker:

```bash
uv sync && uv run uvicorn internship_email_tracker.app:app --reload
```

```bash
cd frontend && pnpm install && pnpm run dev
```

## Gmail API setup

1. Enable the Gmail API in the [Google Cloud Console](https://console.cloud.google.com/) and create OAuth credentials (Desktop app).
2. Save the downloaded JSON as `credentials/client_secret.json`.
3. Run the app once, it'll open a browser to authorize, then save `credentials/token.json` for future runs.