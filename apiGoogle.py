from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']




def login():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def findOrCreateFolder(creds):
    page_token = None
    drive_service = build('drive','V3',credentials=creds)

    while True:
        response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            if file.get('name').find('projet-iot') != -1 and file.get('name')[-10:] == datetime.today().strftime('%Y-%m-%d'):
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                return file.get('id')

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    file_metadata = {
        'name': 'projet-iot'+datetime.today().strftime('%Y-%m-%d'),
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))
    return file.get('id')

#path a mettr en params
def createFile(creds,name):
    drive_service = build('drive','V3',credentials=creds)

    folderId = findOrCreateFolder(creds)
    file_metadata = {
        'name': name,
        'parents': [folderId]
    }
    media = MediaFileUpload('files/'+name+'.jpeg',
                            mimetype='image/jpeg',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    creds = login()
    createFile(creds,'2022-03-10')