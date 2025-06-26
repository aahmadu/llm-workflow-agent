import os
import base64
import email
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Minimal Gmail read scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "gmail_integration/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_latest_unread_email():
    service = get_service()
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        return {"subject": None, "body": None}

    msg = service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()
    headers = msg['payload'].get('headers', [])
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')

    # Handle plain text email body
    parts = msg['payload'].get('parts', [])
    body = None
    for part in parts:
        if part['mimeType'] == 'text/plain':
            body_data = part['body']['data']
            body = base64.urlsafe_b64decode(body_data.encode('UTF-8')).decode('utf-8')
            break

    return {"subject": subject, "body": body}
