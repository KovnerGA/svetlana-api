from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import json

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'svetlana_service_key.json'
FOLDER_NAME = 'Svetlana_Journals_Global'

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def get_or_create_folder(service):
    results = service.files().list(q=f"name='{FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder'").execute()
    folders = results.get('files', [])
    if folders:
        return folders[0]['id']
    metadata = {'name': FOLDER_NAME, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = service.files().create(body=metadata, fields='id').execute()
    return folder['id']

def update_journal(user_id, session_data):
    service = get_drive_service()
    folder_id = get_or_create_folder(service)
    filename = f"journal_{user_id}.json"
    query = f"name='{filename}' and '{folder_id}' in parents"
    response = service.files().list(q=query).execute()
    files = response.get('files', [])
    if files:
        file_id = files[0]['id']
        existing = service.files().get_media(fileId=file_id).execute()
        journal = json.loads(existing)
    else:
        journal = {"sessions": []}
        file_id = None

    journal["sessions"].append(session_data)
    media = MediaInMemoryUpload(json.dumps(journal).encode(), mimetype='application/json')

    if file_id:
        service.files().update(fileId=file_id, media_body=media).execute()
    else:
        metadata = {
            'name': filename,
            'parents': [folder_id],
            'mimeType': 'application/json'
        }
        service.files().create(body=metadata, media_body=media).execute()