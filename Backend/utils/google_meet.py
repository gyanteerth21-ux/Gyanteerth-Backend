"""
Google Meet URL Generator
--------------------------
Uses Google OAuth2 credentials + Google Calendar API to automatically
create a Google Meet link with the given start/end times.

Credential loading priority:
  1. GOOGLE_TOKEN_JSON env var  — full token.json content as a string (for deployment)
  2. token.json file on disk    — auto-detected one level above Backend/ (for local dev)

The refresh_token inside the credentials keeps them alive indefinitely.
If the access token expires, it is silently refreshed before use.
"""

import os
import json
from datetime import datetime, timezone
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import dotenv

dotenv.load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]

# Fallback file path: one level above Backend/ (local dev)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_TOKEN_FILE = os.path.abspath(os.path.join(_BASE_DIR, "..", "token.json"))


def _load_credentials() -> Credentials:
    """
    Load Google OAuth2 credentials.

    Tries GOOGLE_TOKEN_JSON env var first (deployment-safe).
    Falls back to token.json file on disk (local dev).
    Auto-refreshes expired access tokens and persists the refresh.
    """
    token_json_str = os.getenv("GOOGLE_TOKEN_JSON", "").strip()

    if token_json_str:
        # --- Env-var path (deployment) ---
        # Parse the JSON string into a dict
        token_data = json.loads(token_json_str)
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # access token is refreshed in memory — refresh_token stays valid forever
            print("[google_meet] Access token refreshed from env var credentials.")

    else:
        # --- File path (local dev) ---
        token_path = _DEFAULT_TOKEN_FILE
        if not os.path.exists(token_path):
            raise FileNotFoundError(
                f"Google token not found. Set GOOGLE_TOKEN_JSON in your .env, "
                f"or ensure token.json exists at: {token_path}"
            )

        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Persist refreshed token back to disk
            with open(token_path, "w") as f:
                f.write(creds.to_json())

    return creds


def create_google_meet(
    title: str,
    start_time: datetime,
    end_time: datetime,
    timezone_str: str = "Asia/Kolkata",
) -> str:
    """
    Creates a Google Calendar event with an auto-generated Google Meet conference link.

    Args:
        title:        Event/session title shown on Google Calendar.
        start_time:   Event start (aware or naive datetime; naive treated as UTC).
        end_time:     Event end (aware or naive datetime).
        timezone_str: IANA timezone string, default 'Asia/Kolkata'.

    Returns:
        str: The Google Meet join URL (e.g. https://meet.google.com/xxx-xxxx-xxx)

    Raises:
        FileNotFoundError: Credentials not configured.
        Exception: Any Google API or credential error.
    """
    creds = _load_credentials()
    service = build("calendar", "v3", credentials=creds)

    def _fmt(dt: datetime) -> str:
        """Format datetime to RFC3339 string. Naive datetimes treated as UTC."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()

    event = {
        "summary": title,
        "start": {
            "dateTime": _fmt(start_time),
            "timeZone": timezone_str,
        },
        "end": {
            "dateTime": _fmt(end_time),
            "timeZone": timezone_str,
        },
        "conferenceData": {
            "createRequest": {
                "requestId": f"gyanteerth-{os.urandom(8).hex()}",
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
            }
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1,
    ).execute()

    # Extract the Google Meet join URL
    meet_link = (
        created_event
        .get("conferenceData", {})
        .get("entryPoints", [{}])[0]
        .get("uri", "")
    )

    if not meet_link:
        raise Exception("Google Meet link was not returned by the Calendar API.")

    return meet_link
