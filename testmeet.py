from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json

app = FastAPI()

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

CLIENT_SECRETS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

REDIRECT_URI = r"http://localhost:8000/callback"


@app.get("/login")
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    return RedirectResponse(auth_url)


@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(code=code, include_client_id=True)

    creds = flow.credentials

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

    return {"message": "Authentication successful. Now call /create-meet"}


@app.get("/create-meet")
def create_meet():
    if not os.path.exists(TOKEN_FILE):
        return {"error": "Please login first at /login"}

    from google.oauth2.credentials import Credentials

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'jayaraj Meeting',
        'start': {
            'dateTime': '2026-03-25T10:00:00+05:30',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': '2026-03-25T11:00:00+05:30',
            'timeZone': 'Asia/Kolkata',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'meet-' + str(os.urandom(8).hex()),
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    meet_link = event['conferenceData']['entryPoints'][0]['uri']

    return {
        "message": "Meeting created successfully",
        "meet_link": meet_link
    }

