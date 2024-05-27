from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import sys
import os
import gspread
import re

sys.path.append('C:/Python39/Lib/site-packages')


load_dotenv()


def get_worksheet(worksheet_name):
    if worksheet_name=="urls_sheet":
        sheet_url = os.getenv(worksheet_name)
    else:
        sheet_url=get_sheet_url(worksheet_name)

    if sheet_url is None:
        return None
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


def get_sheet_url(sheet_name):
    creds_path = "./credentials.json"
    credential = ServiceAccountCredentials.from_json_keyfile_name(creds_path,
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credential)
    sheet_url = os.getenv('urls_sheet')
    worksheet = client.open_by_url(sheet_url)
    worksheet = worksheet.get_worksheet(0)
    values = worksheet.get_all_values()
    for row in values[1:]:
        if row[0] == sheet_name:
            return row[1]
    return None

def create_xlsx_sheet(sheet_name):
    creds_path = "./credentials.json"
    credential = ServiceAccountCredentials.from_json_keyfile_name(creds_path,
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credential)
    spreadsheet = client.create(sheet_name)
    email_addresses = ['dashboard@dashboard-msit.iam.gserviceaccount.com']
    for mail in email_addresses:
        spreadsheet.share(mail, perm_type='user', role='writer')
    spreadsheet_url = spreadsheet.url
    print("Spreadsheet URL:", spreadsheet_url)
    return spreadsheet_url


def validate_fields(name, id_number, phone_number):
    if not re.fullmatch(r"[A-Za-z\s]+", name):
        return False
    if not (re.fullmatch(r"\d{10}", str(id_number)) and re.fullmatch(r"\d{10}", str(phone_number))):
        return False
    return True

# def give_access(sheet_name):
#     creds_path = "./credentials.json"
#     credential = ServiceAccountCredentials.from_json_keyfile_name(creds_path,
#                                                               ["https://spreadsheets.google.com/feeds",
#                                                                "https://www.googleapis.com/auth/spreadsheets",
#                                                                "https://www.googleapis.com/auth/drive.file",
#                                                                "https://www.googleapis.com/auth/drive"])
#     client = gspread.authorize(credential)
#     worksheet = client.open_by_url(get_sheet_url(sheet_name))
#     worksheet.share("dasarijayakrishna4321@msitprogram.net", perm_type='user', role='writer')