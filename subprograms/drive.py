 # Google API
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
 # Used to download files (Not official Google API so files must be public)
import gdown # Note: I edited the local gdown installation to effectively remove the download limit of 50 files.
 # Also used for file downloads
from subprograms.file_edit import move, delete
#from file_edit import move, delete

def download_file(file_id: str, destination: str) -> None:
    '''
    file_id should be the Google Drive ID of the folder.\n
    destination should be a valid folder.
    '''
    print(f"Next file: {file_id}")
    #file_name = gdown.download(f"https://drive.google.com/uc?/export=download&id={file_id}", quiet=True)
    file_name = gdown.download(f"https://drive.google.com/uc?id={file_id}", quiet=True)
    print(f"Loaded {file_name}")
    if file_name != None:
        move(file_name, f"{destination}/{file_name}")
    return

def download_folder(folder_id: str, folder_name: str, destination: str) -> None:
    '''
    folder_id should be the Google Drive ID of the folder.\n
    folder_name can be anything. It will determine the folder's name once downloaded.\n
    destination should be a valid folder, which will become the parent folder.
    '''
    file_list = gdown.download_folder(f"https://drive.google.com/drive/u/0/folders/{folder_id}")
    if "/" in file_list[0]:
        slash = "/"
    else:
        slash = "\\"
    for i in file_list:
        if i.rfind(slash) > -1:
            file_name = i[i.rfind(slash)+1:]
        else:
            file_name = i[i.rfind(slash)+1:]
        move(i, f"{destination}{slash}{folder_name}")
    folder_to_delete = file_list[0][:file_list[0].rfind(slash)]
    folder_to_delete = folder_to_delete[folder_to_delete.rfind(slash)+1:]
    delete(folder_to_delete)
    return

def download_contents(folder_id: str, destination: str, scopes: list, token_location: str, credentials_location: str) -> None:
    '''
    Downloads all files from the folder specified by folder_id to destination.
    '''
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_location):
        creds = Credentials.from_authorized_user_file(token_location, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_location, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_location, "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("drive", "v3", credentials=creds)
        # Get IDs of all images in folder
        pageToken = ""
        while pageToken is not None:
            response = service.files().list(q=f"'{folder_id}' in parents", pageSize=1000, pageToken=pageToken, fields="nextPageToken, files(id, name)").execute()
            curr_file = response.get('files', [])
            print("file list", curr_file)
            pageToken = response.get("nextPageToken")
            if type(curr_file) == list:
                for i in curr_file:
                    download_file(i["id"], destination)
            else:
                print(curr_file)
                input("curr_file acting up again")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    download_contents(
        "1Z1m4YpNDJfXeMwQCWEuHRK1p8On-Qr09", 
        "eu4_mods/monumental/temp", 
        ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"], 
        "eu4_mods/monumental/subprograms/data/token.json", 
        "eu4_mods/monumental/subprograms/data/credentials.json"
    )
