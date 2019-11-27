import csv
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from gacollector.settings.constants import ENC_OUT
from gacollector.settings.constants import GSHEET_SCOPES, GSHEET_CREDS, GSHEET_TOKEN


class Gsheet:
    def __init__(self):
        self.srv = None
        self.auth()

    def auth(self):
        creds = None
        # The file user_token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(GSHEET_TOKEN):
            with open(GSHEET_TOKEN, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GSHEET_CREDS, GSHEET_SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(GSHEET_TOKEN, 'wb') as token:
                pickle.dump(creds, token)

        self.srv = build('sheets', 'v4', credentials=creds)

    def read(self, spreadsheet_id, range_name):
        book = self.srv.spreadsheets()
        result = book.values().get(spreadsheetId=spreadsheet_id,
                                   range=range_name).execute()
        values = result.get('values', [])
        return values

    def append_rows(self, spreadsheet_id, range_name, values):
        body = {
            'values': values
        }
        result = self.srv.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        # return result.get('updates').get('updatedCells')
        print(result)
        return result.get('updates').get('updatedRows')

    def send_from_csv(self, path_to_csv, spreadsheet_id, range_name):
        with open(path_to_csv, 'r', encoding=ENC_OUT) as f:
            reader = csv.reader(f, dialect='ga')
            values = list(reader)
            return self.append_rows(spreadsheet_id, range_name, values)


if __name__ == '__main__':
    gsheet = Gsheet()

    test_sheet = '1Ya4wunyLZsEObvnadVmD0fRrW7xwj_gwGF5yCzsp6vk'
    test_range = 'A1:L200'

    gsheet.send_from_csv('./test_inc.csv', test_sheet, test_range)
    # res = gsheet.read(test_sheet, test_range)
