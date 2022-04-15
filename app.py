from __future__ import print_function
from fileinput import filename

import os
import requests as re
import re as r

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from apiclient import errors

from appConfig import urls
from appConfig import destinyFolderID

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def mainProcess():
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

    try:

    # Realiza o download das planilhas.

        for url in urls:
            data = re.get(url)
            headerData = data.headers['content-disposition']
            titleRaw = r.findall("filename=(.+)", headerData)[0]
            fileName = r.findall(r'"(.*?)"', titleRaw)[0]
            open(fileName, 'wb').write(data.content)
            existingFilesIDArray = []
            existingFilesNameArray = []

            # Call the Drive v3 API

            service = build('drive', 'v3', credentials=creds)

            page_token = None
            while True:
                response = service.files().list(q=f"mimeType='text/csv' and name='{fileName}' and trashed=false and '{destinyFolderID}' in parents",
                                                    spaces='drive',
                                                    fields='nextPageToken, files(id, name)',
                                                    pageToken=page_token).execute()
                for file in response.get('files', []):
                    existingFilesIDArray.append(file.get('id'))
                    existingFilesNameArray.append(file.get('name'))

                print(existingFilesNameArray)
                print(existingFilesIDArray)

                if len(existingFilesIDArray) > 1:
                    for existingFile in existingFilesIDArray:
                        service.files().delete(fileId=existingFile).execute()
                        print('Deletei um arquivo!')

                    # Upload do arquivo da vez

                    file_metadata = {'name': fileName, 'parents': [destinyFolderID]}
                    media = MediaFileUpload(f'./{fileName}', mimetype='text/csv', resumable=True)
                    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                    print('Fiz um upload!')

                if len(existingFilesIDArray) == 1:

                    # File's new content.
                    media_body = MediaFileUpload(
                        fileName, mimetype='text/csv', resumable=True)

                    # Send the request to the API.
                    service.files().update(
                        fileId=f'{existingFilesIDArray[0]}',
                        media_body=media_body).execute()
                    print('Fiz um update!')

                if len(existingFilesIDArray) == 0:
                    # Upload do arquivo da vez

                    file_metadata = {'name': fileName, 'parents': [destinyFolderID]}
                    media = MediaFileUpload(f'./{fileName}', mimetype='text/csv', resumable=True)
                    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                    print('Fiz um upload!') 

                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            # Deleta os arquivos CSV.

            os.remove(fileName)


    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


mainProcess()