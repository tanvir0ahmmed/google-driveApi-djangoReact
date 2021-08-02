from __future__ import print_function
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#file_id = '17gwZqbdzMW621aHEK_wWb6_gGNMuECVG'

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly'
    ]
def access():
    creds = None
    dic_email = {}
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        print('1')
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('2')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            print(creds)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    file_dic = {}
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            file_dic[item['name']] = item['id']
            print(u'{0} ({1})'.format(item['name'], item['id']))
        print(file_dic)

access()