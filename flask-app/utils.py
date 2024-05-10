import csv
import smtplib
import os
import pickle

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request


load_dotenv(verbose=True)


def user_exists(email):
    with open('./users/users.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                return True
    return False


def get_unregistered_users(users):
    spreadsheets_service = create_spreadsheets_service(
        'sheets', ['https://www.googleapis.com/auth/spreadsheets'])
    result_input = spreadsheets_service.values().get(spreadsheetId=os.environ.get('SPREADSHEET_ID_ROLES'),
                                                     range='A1:AA1000').execute()
    values = result_input.get('values', [])

    user_emails = [user[1] for user in values]
    for user in users:
        if user[1] in user_emails:
            users.remove(user)
    return users


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
    message = f"""Dear {username}
    Congratulations! You succesfully registed at MSIT Dashboard


    Thanks,
    MSIT Admin
    """
    text = f'Subject: {subject}\n\n{message}'
    server.sendmail(from_email, to_email, text)
    server.quit()


def create_spreadsheets_service(api_service_name, *scopes):
    SCOPES = [scope for scope in scopes[0]]

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

    service = build(api_service_name, 'v4', credentials=creds)
    return service.spreadsheets()


def write_users_to_excel(user_list):
    spreadsheets_service = create_spreadsheets_service(
        'sheets', ['https://www.googleapis.com/auth/spreadsheets'])
    spreadsheets_service.values().append(
        spreadsheetId=os.environ.get('SPREADSHEET_ID_ROLES'),
        range='A1:F',  # Assuming your data starts from column A and you want to append to the end of the sheet
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=dict(
            majorDimension='ROWS',
            values=user_list)
    ).execute()
