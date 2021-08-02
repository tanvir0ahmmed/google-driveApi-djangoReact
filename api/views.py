from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permission import Permission
import json
import os.path
from urllib.parse import urlencode
import hashlib

import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleDrive import settings
from django.http import HttpResponse, HttpResponseRedirect

pr = Permission()

class Auth(APIView):
    def get(self, request):
        dic = {}
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
            ]
        GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        params = {
            'client_id': "791937199185-eglh4k4gi7ghamn847ibvoncqdr3v9ea.apps.googleusercontent.com",
            'response_type': 'code',
            'scope': SCOPES,
            'redirect_uri': "http://127.0.0.1:8000/callback/",
            'state': state,
        }
        creds = None
        dic_email = {}
        return HttpResponseRedirect("%s?%s" % (GOOGLE_AUTH_ENDPOINT, urlencode(params)))
            


class Create(APIView):
    def post(self, request, format=None):
        print('hello',request.data, type(request.data))
        #request_data = json.loads(request.data)
        request_data = {}
        request_data['email'] = request.data.get('email')
        request_data['filename'] = request.data.get('filename')
        request_data['read_write'] = request.data.get('read_write')
        #request_data = dict(request.iterlists())
        status = search_mail(request_data['email'],request_data['filename'],request_data['read_write'])
        print(status)
        return Response( {'email': request_data['email'],
            'filename': request_data['filename']})
        

class Delete(APIView):
    def post(self, request, format=None):
        request_data = {}
        request_data['email'] = request.data.get('email')
        request_data['filename'] = request.data.get('filename')
        print(request_data)
        status = del_mail(request_data['email'], request_data['filename'])
        print(status)
        return Response( {'email': request_data['email'],
            'fileEmail': request_data['filename']})
        
class Callback(APIView):
    class Callback(APIView):
        def get(self,request):
            print('Callback')
            return Response(request.data)
        
def del_mail(email,file_name):
    if os.path.exists('email_list.txt'):
        with open('data.txt') as json_file:
            data = json.load(json_file)
        with open('email_list.txt') as json_file:
            dic_email1 = json.load(json_file)
        file_title = list(data.keys())
        file_id = list(data.values())
        if file_name in file_title:
            status = pr.revoke(data[file_name], dic_email1[email],email)
        else:
            status = 'File/Folder not exist'
    else:
        status = 'Email not exist'
    return status

def search_mail(email,file_name,role):
    status = pr.create_permission(email,file_name,role)
    """ if os.path.exists('data.txt'):
        with open('data.txt') as json_file:
            data = json.load(json_file)
        file_title = list(data.keys())
        file_id = list(data.values())
        if file_name in file_title:
            status = pr.create_permission(email,data[file_name],role)
        else:
            status = 'File/Folder not exist'
    else:
        status = pr.create_permission(email,file_name,role) """
    return status
    #print(file_id,file_title)