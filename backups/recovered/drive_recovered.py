 # Google API
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
 # Used to download files (Not official Google API so files must be public)
import gdown
 # Also used for file downloads
from subprograms.file_edit import move as move_file

def download_file(file_id: str, file_name: str, destination: str) -> None:
    '''
    file_data should be formatted as {"id": "example_id", "name", "example_name"}.\n
    dest should be a valid file path.
    '''
    url = "https://drive.google.com/uc?/export=download&id="
    print(file_id, file_name)
    print(f"{url}{file_id}")
    gdown.download(f"{url}{file_id}")
    move_file(file_name, f"{destination}/{file_name}")
    return

def download_folder(folder_id: str, destination: str, scopes: list, token_location: str, credentials_location: str) -> None:
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
        items = []
        pageToken = ""
        while pageToken is not None:
            response = service.files().list(q=f"'{folder_id}' in parents", pageSize=1000, pageToken=pageToken, fields="nextPageToken, files(id, name)").execute()
            curr_file = response.get('files', [])
            #items.extend(curr_file)
            #pageToken = response.get("nextPageToken")
            #print("--", curr_file)
            if type(curr_file) == list:
                for i in curr_file:
                    download_file(i["id"], i["name"], destination)
            else:
                print(curr_file)
                input("curr_file acting up again")
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    download_folder()