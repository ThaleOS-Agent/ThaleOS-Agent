"""
ThaleOS Google Calendar Connector
OAuth 2.0 flow, token storage (encrypted at rest), event CRUD.

Setup required:
1. Create a Google Cloud project
2. Enable the Google Calendar API
3. Create OAuth 2.0 credentials (type: "Web application")
4. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
5. Add http://localhost:8099/api/calendar/callback as an authorised redirect URI
"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger("ThaleOS.Calendar")

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8099/api/calendar/callback")
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# Fernet encryption for token storage
def _get_fernet():
    from cryptography.fernet import Fernet
    import base64, hashlib
    secret = os.getenv("JWT_SECRET_KEY", "thaleos-dev-secret-change-in-production-32chars")
    key = base64.urlsafe_b64encode(hashlib.sha256(secret.encode()).digest())
    return Fernet(key)


class GoogleCalendarConnector:
    """
    Manages Google Calendar OAuth tokens per user and provides
    event CRUD operations.
    """

    def __init__(self):
        import db as _db
        self._db = _db

    # ── OAuth flow ────────────────────────────────────────────────────────────

    def start_oauth_flow(self, user_id: str) -> str:
        """
        Returns the Google OAuth authorisation URL.
        The user should be redirected here.
        """
        if not CLIENT_ID:
            raise ValueError("GOOGLE_CLIENT_ID is not set in .env")

        from google_auth_oauthlib.flow import Flow
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [REDIRECT_URI],
                }
            },
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            state=user_id,
            prompt="consent",
        )
        return auth_url

    def handle_oauth_callback(self, user_id: str, code: str) -> dict:
        """
        Exchange authorisation code for tokens and store encrypted in DB.
        Returns the token info dict.
        """
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [REDIRECT_URI],
                }
            },
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        flow.fetch_token(code=code)
        creds = flow.credentials

        token_data = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes) if creds.scopes else SCOPES,
        }
        self._save_tokens(user_id, token_data)
        logger.info(f"[calendar] OAuth tokens saved for user {user_id}")
        return {"status": "connected", "user_id": user_id}

    # ── Token storage ─────────────────────────────────────────────────────────

    def _save_tokens(self, user_id: str, token_data: dict) -> None:
        fernet = _get_fernet()
        encrypted = fernet.encrypt(json.dumps(token_data).encode()).decode()
        now = datetime.now(timezone.utc).isoformat()

        existing = self._db.fetchone(
            "SELECT id FROM integrations WHERE user_id = ? AND provider = ?",
            (user_id, "google_calendar"),
        )
        if existing:
            self._db.execute(
                "UPDATE integrations SET config = ?, updated_at = ? WHERE user_id = ? AND provider = ?",
                (encrypted, now, user_id, "google_calendar"),
            )
        else:
            self._db.execute(
                "INSERT INTO integrations (id, user_id, provider, config, created_at, updated_at) VALUES (?,?,?,?,?,?)",
                (f"gcal_{user_id}", user_id, "google_calendar", encrypted, now, now),
            )

    def _load_tokens(self, user_id: str) -> Optional[dict]:
        row = self._db.fetchone(
            "SELECT config FROM integrations WHERE user_id = ? AND provider = ?",
            (user_id, "google_calendar"),
        )
        if not row:
            return None
        fernet = _get_fernet()
        return json.loads(fernet.decrypt(row["config"].encode()))

    def _build_service(self, user_id: str):
        """Build and return an authorized Google Calendar API service."""
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        token_data = self._load_tokens(user_id)
        if not token_data:
            raise ValueError(f"No Google Calendar tokens for user {user_id}")

        creds = Credentials(
            token=token_data["token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
            client_id=token_data.get("client_id", CLIENT_ID),
            client_secret=token_data.get("client_secret", CLIENT_SECRET),
            scopes=token_data.get("scopes", SCOPES),
        )

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token_data["token"] = creds.token
            self._save_tokens(user_id, token_data)

        return build("calendar", "v3", credentials=creds)

    def is_connected(self, user_id: str) -> bool:
        return self._load_tokens(user_id) is not None

    # ── Calendar CRUD ─────────────────────────────────────────────────────────

    def list_events(self, user_id: str, days: int = 7) -> list[dict]:
        """Return events for the next `days` days."""
        service = self._build_service(user_id)
        now = datetime.now(timezone.utc)
        time_min = now.isoformat()
        time_max = (now + timedelta(days=days)).isoformat()

        result = service.events().list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
            maxResults=50,
        ).execute()

        events = []
        for item in result.get("items", []):
            start = item.get("start", {})
            end = item.get("end", {})
            events.append({
                "id": item["id"],
                "title": item.get("summary", "(No title)"),
                "start": start.get("dateTime", start.get("date")),
                "end": end.get("dateTime", end.get("date")),
                "description": item.get("description", ""),
                "location": item.get("location", ""),
                "status": item.get("status", "confirmed"),
            })
        return events

    def create_event(self, user_id: str, event: dict) -> dict:
        """
        Create a new event.
        event dict: { title, start (ISO), end (ISO), description?, location? }
        Returns the created event with its Google ID.
        """
        service = self._build_service(user_id)
        body = {
            "summary": event["title"],
            "start": {"dateTime": event["start"], "timeZone": "UTC"},
            "end": {"dateTime": event["end"], "timeZone": "UTC"},
        }
        if event.get("description"):
            body["description"] = event["description"]
        if event.get("location"):
            body["location"] = event["location"]

        created = service.events().insert(calendarId="primary", body=body).execute()
        logger.info(f"[calendar] Event created: {created['id']} for user {user_id}")
        return {
            "id": created["id"],
            "title": created.get("summary"),
            "start": created.get("start", {}).get("dateTime"),
            "end": created.get("end", {}).get("dateTime"),
            "html_link": created.get("htmlLink"),
        }

    def update_event(self, user_id: str, event_id: str, changes: dict) -> dict:
        """Patch an existing event."""
        service = self._build_service(user_id)
        patch = {}
        if "title" in changes:
            patch["summary"] = changes["title"]
        if "start" in changes:
            patch["start"] = {"dateTime": changes["start"], "timeZone": "UTC"}
        if "end" in changes:
            patch["end"] = {"dateTime": changes["end"], "timeZone": "UTC"}
        if "description" in changes:
            patch["description"] = changes["description"]

        updated = service.events().patch(
            calendarId="primary", eventId=event_id, body=patch
        ).execute()
        return {"id": updated["id"], "status": "updated"}

    def delete_event(self, user_id: str, event_id: str) -> None:
        """Delete an event by ID."""
        service = self._build_service(user_id)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        logger.info(f"[calendar] Event deleted: {event_id} for user {user_id}")

    def check_conflicts(self, user_id: str, start: str, end: str) -> list[dict]:
        """
        Return any events that overlap with the given time window.
        Used by ChronaGate to prompt for approval before scheduling.
        """
        service = self._build_service(user_id)
        result = service.events().list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
        ).execute()
        return [
            {
                "id": e["id"],
                "title": e.get("summary", "(No title)"),
                "start": e.get("start", {}).get("dateTime", e.get("start", {}).get("date")),
                "end": e.get("end", {}).get("dateTime", e.get("end", {}).get("date")),
            }
            for e in result.get("items", [])
        ]


# ── Background sync ───────────────────────────────────────────────────────────

async def sync_all_users(calendar_connector: GoogleCalendarConnector) -> None:
    """
    APScheduler job: sync Google Calendar events for all connected users
    into the local schedule_items table.
    """
    import db
    rows = db.fetchall("SELECT DISTINCT user_id FROM integrations WHERE provider = 'google_calendar'")
    for row in rows:
        uid = row["user_id"]
        try:
            events = calendar_connector.list_events(uid, days=14)
            now = datetime.now(timezone.utc).isoformat()
            for evt in events:
                existing = db.fetchone(
                    "SELECT id FROM schedule_items WHERE external_id = ? AND user_id = ?",
                    (evt["id"], uid),
                )
                if not existing:
                    db.execute(
                        "INSERT OR IGNORE INTO schedule_items (id, user_id, title, description, start_time, end_time, calendar_provider, external_id, status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (
                            f"gcal_{evt['id']}",
                            uid,
                            evt["title"],
                            evt.get("description", ""),
                            evt["start"],
                            evt["end"],
                            "google",
                            evt["id"],
                            "scheduled",
                            now,
                        ),
                    )
            logger.info(f"[calendar] Synced {len(events)} events for user {uid}")
        except Exception as e:
            logger.warning(f"[calendar] Sync failed for user {uid}: {e}")
