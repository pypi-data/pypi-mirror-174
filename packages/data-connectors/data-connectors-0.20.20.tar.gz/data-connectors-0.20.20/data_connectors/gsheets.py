import os
import pygsheets
import pandas as pd
from pygsheets import DataRange

from .creds import load_creds
load_creds()

class Gsheets:
    """
    Pass in a service account file path and query data stored in Google Sheets
    Example: Gsheets('SPREADSHEET').query('WORKSHEET')
    """
    def __init__(self, spreadsheet):
        self.client = pygsheets.authorize(service_file=(os.getenv("GSHEETS_SERVICE_ACCOUNT")))
        self.spreadsheet_key = os.getenv(spreadsheet)
        self.spreadsheet = self.client.open_by_key(self.spreadsheet_key)

    def query(self, worksheet, start_cell=None, end_cell=None):
        """
        Returns results of spreadsheet, worksheet as a pandas DataFrame
        Spreadsheet is stored as env var
        Worksheet is passed in as plain text
        """        
        ws = self.spreadsheet.worksheet_by_title(worksheet)
        df = ws.get_as_df(start=start_cell, end=end_cell)
        print(f"{self.spreadsheet.title}.{worksheet}: Downloaded {df.shape} shape")
        return df

    # If get_as_df does not work, use this instead
    def select_all_values(self, worksheet):
        return pd.DataFrame(
            self.spreadsheet.worksheet_by_title(worksheet).get_all_records()
        )

    def write_df(self, df, worksheet, start_cell='A1'):
        self.spreadsheet.worksheet_by_title(worksheet).set_dataframe(df, start=start_cell)

    def write_df_with_timestamp(self, df, worksheet):
        # Reference the worksheet by title
        worksheet = self.spreadsheet.worksheet_by_title(worksheet)
        # Clear existing data
        worksheet.clear(start='A1')
        # Write the frame to the worksheet, adding rows if necessary
        worksheet.set_dataframe(df, start="A1", extend=True)
        # Resize the worksheet to the shape of the frame
        worksheet.resize(rows=df.shape[0]+1, cols=df.shape[1])
        # Add borders
        drange = DataRange(start='A1', worksheet=worksheet)
        drange.update_borders(top=True, right=True, bottom=True, left=True, inner_horizontal=True, inner_vertical=True, style='SOLID')
        # Complete message
        print(f"Wrote {len(df)} rows to {self.spreadsheet.title}.{worksheet.title}")