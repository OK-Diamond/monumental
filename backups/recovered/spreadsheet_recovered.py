from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build # pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.errors import HttpError

def retrieve_range(spreadsheet_id: str, range_name: str, scopes: list, token_location: str, credentials_location: str) -> list[list[str]]:
    '''
    Retrieves the relevant range from the given spreadsheet.\n
    Data is returned as a list of lists, with each inner list being one row of the spreadsheet.
    '''
    creds = None
    if os.path.exists(token_location):
        creds = Credentials.from_authorized_user_file(token_location, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_location, "w") as token:
            token.write(creds.to_json())
    
    data = []
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return data

        for row in values:
            data.append(row)
            #print(row)
    except HttpError as err:
        print(err)
    return data


if __name__ == "__main__":
    a = retrieve_range("1C1mt8cOGRljZgc5gwC9uRpVlL-XjPQ84Di4g08tNEuo", "Monument type!A1:C")
    for i in a:
        print(i)
        