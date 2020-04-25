from gacollector.connectors.google_sheets_api.base import Gsheet
from gacollector.tasks.base import Task


class GsheetTask(Task):
    def __init__(self, out_csv_path, gsheet_id, gsheet_cell_address):
        self.path_to_csv = out_csv_path
        self.gsheet_id = gsheet_id
        self.gsheet_cell_address = gsheet_cell_address

        self.api = Gsheet()

    def run(self):
        self.api.send_from_csv(self.path_to_csv, self.gsheet_id, self.gsheet_cell_address)
