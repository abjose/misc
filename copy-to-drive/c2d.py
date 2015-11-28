# setup info: https://developers.google.com/drive/web/quickstart/python
# examples: https://developers.google.com/drive/v2/reference/files/list
# this code is mostly lifted from those two places
# you might need to install p7zip-full

from __future__ import print_function
import httplib2
import os
import mimetypes
import subprocess

from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.drive-credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def retrieve_backup_folder_id(service):
    """Retrieve the id of a drive folder called "backups"

    Args:
      service: Drive API service instance.
    Returns:
      THE ID OH MY GOD
    """
    result = None
    param = {}
    param["maxResults"] = 10
    param["q"] = ("title='backups' and " +
                  "mimeType = 'application/vnd.google-apps.folder'")
    try:
        result = service.files().list(**param).execute()
    except errors.HttpError, error:
        print('An error occurred:', error)
        return None
        
    assert(len(result["items"]) == 1)
    return result["items"][0]["id"]
    
def insert_file(service, title, description, parent_id, mime_type, filename):
    """Insert new file.
    
    Args:
      service: Drive API service instance.
      title: Title of the file to insert, including the extension.
      description: Description of the file to insert.
      parent_id: Parent folder's ID.
      mime_type: MIME type of the file to insert.
      filename: Filename of the file to insert.
    Returns:
      Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
        'title': title,
        'description': description,
        'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        file = service.files().insert(body=body,
                                      media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        # print('File ID: %s' % file['id'])

        return file
    except errors.HttpError, error:
        print('An error occured:', error)
        return None

def zip_and_encrypt(files, password, output_name):
    rc = subprocess.call(['7z', 'a', '-p'+password, '-y', output_name] +
                         files)
    
def backup_on_drive(filename):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    backup_folder_id = retrieve_backup_folder_id(service)
    
    if backup_folder_id == None:
        print("Couldn't find backups folder.")
        return
        
    insert_file(service, filename, "something mysterious", backup_folder_id,
                mimetypes.guess_type("filename")[0], filename)

if __name__ == '__main__':
    # probably use absolute paths
    files_to_backup = ["hello.txt",
                       "stuff/*"] 
    archive_name = "./c2d.zip"
    password = "password" # probably change this
    zip_and_encrypt(files_to_backup, password, archive_name)
    backup_on_drive("c2d.zip")
