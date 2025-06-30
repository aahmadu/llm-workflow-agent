from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from pathlib import Path
import base64
import json
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CRED_DIR = Path(__file__).resolve().parent.parent.parent / "credentials"
CREDENTIALS_PATH = CRED_DIR / "credentials.json"
TOKEN_PATH = CRED_DIR / "token.json"

def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def get_latest_unread_emails(n=3):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])[:n]

    emails = []
    for msg in messages:
        full = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = full['payload']

        headers = payload['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "(No Subject)")

        parts = payload.get('parts')
        body = ""

        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body_data = part['body'].get('data')
                    if body_data:
                        decoded = base64.urlsafe_b64decode(body_data).decode()
                        body = decoded
                        break
        else:
            body_data = payload['body'].get('data')
            if body_data:
                decoded = base64.urlsafe_b64decode(body_data).decode()
                body = decoded

        soup = BeautifulSoup(body, 'html.parser')
        clean_body = soup.get_text().strip()

        emails.append({
            "subject": subject,
            "body": clean_body,
        })

    return emails
