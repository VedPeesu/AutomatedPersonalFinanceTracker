from __future__ import print_function
import os
import os.path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import datetime


SCOPES = ["https://www.googleapis.com/auth/drive"]

def auth_google_drive():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def current_month_year():
    current = datetime.datetime.now()
    return current.strftime("%Y_%m")

def upload_to_drive(file_path, folder_id=None):
    creds = auth_google_drive()
    service = build("drive", "v3", credentials=creds)
    month_year = current_month_year()
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    new_file_name = f"{name}_{month_year}{ext}"
    file_data = {'name': new_file_name}
    if folder_id:
        file_data['parents'] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_data, media_body = media, fields='id').execute()
    print(f"File uploaded with ID: {file.get('id')}")

if __name__ == "__main__":
    upload_to_drive('finance.csv')
    upload_to_drive('budget.txt')
    upload_to_drive('category_budgets.txt')
