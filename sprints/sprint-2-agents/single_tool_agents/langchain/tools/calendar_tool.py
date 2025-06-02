from langchain.tools import tool
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@tool
def get_calendar(input: str) -> str:
    """Fetch events from your Google Calendar for a given city and date (format: 'City, YYYY-MM-DD')."""
    try:
        city, date_str = map(str.strip, input.split(","))
        creds = authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)

        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start = datetime.datetime.combine(date, datetime.time.min).isoformat() + 'Z'
        end = datetime.datetime.combine(date, datetime.time.max).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary', timeMin=start, timeMax=end,
            maxResults=10, singleEvents=True, orderBy='startTime').execute()
        
        events = events_result.get('items', [])

        if not events:
            return f"No events found on {date_str}."

        output = f"📅 Events on {date_str}:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No Title')
            output += f"- {summary} at {start}\n"

        return output.strip()

    except Exception as e:
        return f"❌ Error: {e}"
