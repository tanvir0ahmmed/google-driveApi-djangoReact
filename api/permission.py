from __future__ import print_function
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleDrive import settings
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlencode
import hashlib
#file_id = '17gwZqbdzMW621aHEK_wWb6_gGNMuECVG'
dic = {}
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
def access(self,email,file_name,role):
    creds = None
    dic_email = {}
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.credentials, SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    def callback(request_id, response, exception):
        if exception:
            print (exception)
        else:
            #print ("Permission Id: %s %s" % response.get('id') % response.get('email'))
            print('res',response.get('id'), response)
            dic_email[email] = str(response.get('id'))
    service = build('drive', 'v3', credentials=creds)
    print('dic email: ',dic_email)
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    file_dic = {}
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            #print(item)
            file_dic[item['name']] = item['id']
            #print(u'{0} ({1})'.format(item['name'], item['id']))
        #print(file_dic)
        with open('data.txt', 'w') as outfile:
            json.dump(file_dic, outfile)
    with open('data.txt') as json_file:
        data = json.load(json_file)
    file_title = list(data.keys())
    file_id = list(data.values())
    if file_name in file_title:
        file_id = data[file_name]
        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        batch.add(service.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
        ))
        batch.execute()
        if os.path.exists('email_list.txt'):
            with open('email_list.txt') as json_file:
                dic_email1 = json.load(json_file)
            print('dic email1: ',dic_email1)
            dic_email1[email] = dic_email[email]
            

            with open('email_list.txt', 'w') as outfile:
                json.dump(dic_email1, outfile)
        else:
            with open('email_list.txt', 'w') as outfile:
                json.dump(dic_email, outfile)
        status = 'Permission Added'
    else:
        status = 'File/Folder not exist'
    return status

def revoke_permission(self,file_id,pr_id,email):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            # print ("Permission Id: %s" % response.get('id'))
            print("Permission Id: %s" % response)

    batch = service.new_batch_http_request(callback=callback)
    #batch.add(service.permissions().list(fileId=file_id))
    batch.add(service.permissions().delete(fileId=file_id,permissionId=pr_id))
    batch.execute()
    with open('email_list.txt') as json_file:
        dic_email1 = json.load(json_file)
    dic_email1.pop(email, None)
    with open('email_list.txt', 'w') as outfile:
        json.dump(dic_email1, outfile)



class Permission:
    def create_permission(self,email,file_id,role):
        status = access(self,email,file_id,role)
        return status
    def revoke(self,file_id,pr_id,email):
        revoke_permission(self, file_id, pr_id,email)
        return 'Permission Revoke'