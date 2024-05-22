from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import sys
import os
import gspread

sys.path.append('C:/Python39/Lib/site-packages')


load_dotenv()


def get_worksheet(worksheet_name):
    sheet_url = os.getenv(worksheet_name)
    creds_path = "./credentials.json"
    credential = ServiceAccountCredentials.from_json_keyfile_name(creds_path,
                                                                  ["https://spreadsheets.google.com/feeds",
                                                                   "https://www.googleapis.com/auth/spreadsheets",
                                                                   "https://www.googleapis.com/auth/drive.file",
                                                                   "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credential)
    worksheet = client.open_by_url(sheet_url)
    worksheet = worksheet.get_worksheet(0)
    return worksheet
