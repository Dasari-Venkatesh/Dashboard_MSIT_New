import csv
import smtplib
import os
import pickle

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request


load_dotenv(verbose=True)
def user_exists(email):
    with open('./users/users.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                return True
    return False


def send_email(email, username):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    from_email = "jayakrishnad2002@gmail.com"
    to_email = email
    subject = "MSIT Dashboard"
    message = f"""
    Dear {username}
    Congratulations! You succesfully registed at MSIT Dashboard


    Thanks,
    MSIT Admin
    """
    text = f'Subject: {subject}\n\n{message}'

    server.sendmail(from_email, to_email, text)
    server.quit()


def get_data_from_excel(keyword):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    if keyword == 'scores':
        result_input = sheet.values().get(spreadsheetId=os.environ.get('SPREADSHEET_ID'),
                                    range='A1:AA1000').execute()
    elif keyword == 'role':
        result_input = sheet.values().get(spreadsheetId=os.environ.get('SPREADSHEET_ID_ROLES'),
                                    range='A1:AA1000').execute()
    values_input = result_input.get('values', [])

    if not values_input:
        print('No data found.')
        return
    return values_input
