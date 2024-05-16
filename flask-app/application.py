import io
import sys
import os
import csv
import json
import pandas as pd
import datetime

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from collections import OrderedDict
from collections import defaultdict
from utils import user_exists, send_email, create_spreadsheets_service, write_users_to_excel, get_unregistered_users

import sys
sys.path.append('C:/Python39/Lib/site-packages')
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import csv, json
import pandas as pd
from collections import OrderedDict
from collections import defaultdict
import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()
users_sheet_url = os.getenv('users_sheet_url')
scores_sheet_url = os.getenv('scores_sheet_url')
creds_path = "./credentials.json"
credential = ServiceAccountCredentials.from_json_keyfile_name(creds_path,
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
user_worksheet = client.open_by_url(users_sheet_url)
users_worksheet = user_worksheet.get_worksheet(0)
score_worksheet = client.open_by_url(scores_sheet_url)
scores_worksheet = score_worksheet.get_worksheet(0)

sys.path.append('C:/Python39/Lib/site-packages')

app = Flask(__name__)
CORS(app)

IT_course_dates = {
    "IDS":["2020-11-09", "2020-12-05"],
    "PSC":["2020-12-07", "2021-01-02"],
    "ADS":["2021-01-04", "2021-02-06"],
    "CN":["2021-02-08", "2021-02-20"],
    "DB":["2021-02-22", "2021-03-06"],
    "Elective-1/Remedial": ["2021-03-08", "2021-04-03"]
}

SS_course_dates = {
    "SS":["2021-02-08","2021-04-02"]
}


@app.route("/info/<string:student_email>")
def read_folder(student_email):
    result = {}
    path = "./student_score_info/" + student_email + ".json"
    with open(path) as read_file:
        result = json.loads(read_file.read())
    # print(result)
    return jsonify({
        "success": True,
        "dashboard_data": result
    })

@app.route("/zoom_output/<string:student_email>")
def zoom_att(student_email):
    path = "./zoom_output/" + student_email + ".json"
    with open(path) as read_file:
        result = json.loads(read_file.read())
    # print('/n'*5, result, '/n'*5)
    return jsonify({
        "success": True,
        "dashboard_data": result
    })

@app.route("/update_data")
def read_file():
    # print("Hello")
    grades,course_names = get_student_grades()
    ppt_scores = get_presentation_scores()
    data = pd.read_csv("./zoom_attendance_data/zoom_att_IT.csv")
    date = list(data.loc[0].dropna())
    week =  [each for each in list(data.columns) if 'Unnamed' not in each]
    dates = [each for each in date if 'Unnamed' not in each]
    final_dict = {}

    course_stats = {'attendance':{},'grades':{},'cgpa':[]}
    time_to_stop = 0

    # print(len(data.index))
    for i in range(2, len(data.index)):
        row_data = list(data.loc[i])
        row_data_json = {}
        row_data_json['Email'] = row_data[0].lower()
        row_data_json['IT_Mentor'] = row_data[1]
        row_data_json['SS_Mentor'] = row_data[2]
        row_data_json['Center'] = row_data[3]

        j = 4
        k = 0
        weeks_dict = defaultdict(dict)
        week_num = 0
        flag_it = False
        flag_ss = False
        for each in dates:
            if pd.isna(row_data[j]):
                row_data[j] = '-'
            if pd.isna(row_data[j+1]):
                row_data[j+1] = '-'
            if pd.isna(row_data[j+2]):
                row_data[j+2] = '-'
            if pd.isna(row_data[j+3]):
                row_data[j+3] = '-'
            if pd.isna(row_data[j+4]):
                row_data[j+4] = '-'
            if pd.isna(row_data[j+5]):
                row_data[j+5] = '-'
            if pd.isna(row_data[j+6]):
                row_data[j+6] = '-'
            if pd.isna(row_data[j+7]):
                row_data[j+7] = '-'
            if pd.isna(row_data[j+8]):
                row_data[j+8] = '-'
            if pd.isna(row_data[j+9]):
                row_data[j+9] = '-'
            
            if each == '2020-11-25' or flag_it:
                flag_it = True
                if each == '2021-02-08' and not flag_ss:
                    flag_ss = True

                if not flag_ss:
                    row_data_json[each] = {"9:00 AM":row_data[j],"9:00 AM Active minutes":row_data[j+1], "Duration1":row_data[j+2],"11:00 AM":row_data[j+3],"11:00 AM Active minutes":row_data[j+4],"Duration2":row_data[j+5], "Total":row_data[j+6], "2:00 PM": None}
                    j += 7

                else:
                    row_data_json[each] = {"9:00 AM":row_data[j],"9:00 AM Active minutes":row_data[j+1], "Duration1":row_data[j+2],"11:00 AM":row_data[j+3],"11:00 AM Active minutes":row_data[j+4],"Duration2":row_data[j+5], "Total":row_data[j+6], "2:00 PM":row_data[j+7],"2:00 PM Active minutes":row_data[j+8],"Duration3":row_data[j+9]}
                    j += 10
            
            else:
                row_data_json[each] = {"9:00 AM":row_data[j],"9:00 AM Active minutes":row_data[j+1], "11:00 AM":row_data[j+2],"11:00 AM Active minutes":row_data[j+3], "Total":row_data[j+4],"2:00 PM": None}
                j = j + 5

            current_week_data = weeks_dict[week[week_num]]
            if len(current_week_data.keys()) == 5:
                week_num += 1
                weeks_dict[week[week_num]] = {each: row_data_json[each]}
            elif len(current_week_data) == 0:
                weeks_dict[week[week_num]] = {each: row_data_json[each]}
            else:
                current_week_data[each] = row_data_json[each]
                weeks_dict[week[week_num]] = current_week_data
            
        att_grades_data = {'attendance':weeks_dict,"grades":grades[row_data[0].lower()],'ppt_scores':ppt_scores[row_data[0].lower()]}
        course_stats['cgpa'].append(grades[row_data[0].lower()]['CGPA'])

        for course in course_names:
            if course not in course_stats['grades']:
                course_stats['grades'][course] = {}
            temp_grade = grades[row_data[0].lower()][course]['Grade']
            # print(course_stats['grades'][course], temp_grade)
            if temp_grade not in course_stats['grades'][course]:
                course_stats['grades'][course][temp_grade] = 1
            else:
                course_stats['grades'][course][temp_grade] += 1

        for k in IT_course_dates:
            temp = IT_course_dates[k]
            start_year, start_month, start_day = map(int, temp[0].split("-"))
            end_year, end_month, end_day = map(int, temp[1].split("-"))
            start_date_obj = datetime.datetime(start_year, start_month, start_day)
            end_date_obj = datetime.datetime(end_year, end_month, end_day)
            
            score = getPercentage(start_date_obj, end_date_obj, weeks_dict, 'IT')
            if score is not None:
                if k not in course_stats['attendance']:
                    course_stats['attendance'][k] = []
                # course_stats['attendance'][k] = [start_date_obj.strftime('%d/%m/%Y'), end_date_obj.strftime('%d/%m/%Y'), score]
                course_stats['attendance'][k].append(score)

        for course in SS_course_dates:
            temp = SS_course_dates[course]
            start_year, start_month, start_day = map(int, temp[0].split("-"))
            end_year, end_month, end_day = map(int, temp[1].split("-"))
            start_date_obj = datetime.datetime(start_year, start_month, start_day)
            end_date_obj = datetime.datetime(end_year, end_month, end_day)
            
            score = getPercentage(start_date_obj, end_date_obj, weeks_dict, 'SS')
            if score is not None:
                if course not in course_stats['attendance']:
                    course_stats['attendance'][course] = []
                # course_stats['attendance'][course] = [start_date_obj.strftime('%d/%m/%Y'), end_date_obj.strftime('%d/%m/%Y'), score]
                course_stats['attendance'][course].append(score)

        print(row_data[0].lower())

        with open('./zoom_output/'+ row_data[0].lower()+'.json', "w") as outfile:
            outfile.write(json.dumps(att_grades_data))
        
        # time_to_stop += 1
        # if time_to_stop == 5:
        #     break

    # print(course_stats)
    # print(len(course_stats['cgpa']))

    return jsonify({
        "success": True,
        "data": "successfully updated"
    })

def get_student_grades():
    data_iiit = pd.read_csv("./zoom_attendance_data/CGPA_IIIT.csv")
    data_jntu = pd.read_csv("./zoom_attendance_data/CGPA_JNTU.csv")
    data = pd.concat([data_iiit[:-6],data_jntu[1:]], ignore_index = True)
    course_names =  [each for each in list(data.columns) if 'Unnamed' not in each]
    column_names = list(data.loc[0].dropna())

    grades = {}

    for student in range(1,len(data.index)):
        row_data = list(data.loc[student])
        row_data_json = {}
        row_data_json['Sno'] = row_data[0]
        row_data_json['roll_number'] = row_data[1]
        row_data_json['student_name'] = row_data[2]
        # print(row_data[3])
        row_data_json['student_email'] = row_data[3].lower()
        row_data_json['learning_center'] = row_data[4].lower()
        row_data_json['CGPA'] = row_data[5]

        j = 6
        for course in course_names:
            row_data_json[course] = {"Credits":row_data[j],"Points":row_data[j+1],"Grade":row_data[j+2],"Mentor":row_data[j+3]}
            j += 4
        grades[row_data[3].lower()] = row_data_json
    return grades,course_names

def getPercentage(start_date, end_date, data, info_type):
    # print('The start date and the end date: ', start_date, end_date, data)
    
    weeks_list = list(data.keys())[::-1]
    course_score = 0
    total_count = 0         # To keep track of the total sessions
    
    for week in weeks_list:
        week_data = data[week]
        
        for date in week_data:
            year, month, day = map(int,date.split('-'))
            
            date_obj = datetime.datetime(year, month, day)
            
            if date_obj >= start_date and date_obj <= end_date:
                # Compute the score
                if info_type == 'IT':
                    current_total = week_data[date]['Total']
                else:
                    current_total = week_data[date]['2:00 PM']
                
                if current_total != '-':
                    course_score += float(current_total)
                    total_count += 1
                    
            # the break condition
            if date_obj < start_date:
                break
        else:
            continue
        
        break
    # print("The result: ", course_score, total_count)
    try:
        result = (course_score / total_count) * 100
    except Exception as e:
        # print(e)
        return None
    return round(result,2)

def get_presentation_scores():
    data_iiit = pd.read_csv("./zoom_attendance_data/PresentationScores_IIITH.csv")
    data_jntu = pd.read_csv("./zoom_attendance_data/PresentationScores_JNTUH.csv")
    data = pd.concat([data_iiit,data_jntu], ignore_index = True)
    read_total_number_of_presentations =  [each for each in list(data.columns) if 'Unnamed' not in each]
    total_number_of_presentations = read_total_number_of_presentations[1]
    week_num_list = list(data.loc[0].dropna())
    week_num_list = week_num_list[6:]
    # print(week_num_list)

    ppt_scores = {}

    for student in range(1,len(data.index)):
        row_data = list(data.loc[student])
        row_data_json = {}
        row_data_json['roll_number'] = row_data[0]
        row_data_json['student_email'] = row_data[1].lower()
        row_data_json['num_of_ppt'] = row_data[2]
        row_data_json['total_ppt'] = total_number_of_presentations
        row_data_json['absent'] = row_data[3]
        row_data_json['remedial'] = row_data[4]
        row_data_json['average'] = row_data[5]
        row_data_json['weekly_scores'] = []
        j = 6
        for week_num in week_num_list:
            # print(row_data[j])
            if pd.isna(row_data[j]):
                row_data_json['weekly_scores'].append("No session")
            else:
                row_data_json['weekly_scores'].append(row_data[j])
            j += 1
            
        ppt_scores[row_data[1].lower()] = row_data_json
    
    return ppt_scores




def check_duplicate(email):
    existing_data = users_worksheet.get_all_values()
    existing_emails = [row[0] for row in existing_data]  # Assuming emails are in the first column
    return email in existing_emails

def add_to_google_sheets(values):
    users_worksheet.append_rows(values)


def process_data(data):
    existing_emails = [row[0].lower() for row in users_worksheet.get_all_values()]  # Fetch existing emails from Google Sheet in lowercase
    unique_rows = []
    
    if isinstance(data, dict):  # Single JSON object
        email = data.get('email')
        if email and email.lower() not in existing_emails:  # Convert email to lowercase for comparison
            unique_rows.append(list(data.values()))
    elif isinstance(data, list):  # List of JSON objects
        for entry in data:
            email = entry.get('email')
            if email and email.lower() not in existing_emails:  # Convert email to lowercase for comparison
                unique_rows.append(list(entry.values()))
    else:
        return jsonify({'error': 'Invalid data format'})
    
    if unique_rows:
        add_to_google_sheets(unique_rows)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.csv'):
            reader = list(csv.DictReader(file.read().decode('utf-8').splitlines()))
            print(reader)
            process_data(reader)  
    else:
        try:
            data = json.loads(request.data.decode('utf-8'))
            process_data(data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON data format'})

    return jsonify({'message': 'Data added successfully'})

@app.route('/get_role/<string:email>', methods=['GET'])
def get_role(email):

    if not email:
        return jsonify({'error': 'Email parameter is missing'}), 400
    
    try:
        data = users_worksheet.get_all_records()
        print("Data from Google Sheet:", data)
        for row in data:
            print("Row from Google Sheet:", row)
            if row['email'].lower() == email.lower():
                print(email)
                return jsonify({'role': row['role']})
        
        return jsonify({'error': 'Email not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/student-scores/<string:student_email>')
def student_score(student_email):

    values = scores_worksheet.get_all_values()
    data_json = []

    headers = values[0]
    for row in values[1:]:
        if row[1] == student_email:
            data_json = json.dumps([dict(zip(headers,row))],indent=4)
    if data_json == []:
        return jsonify({'message':"Email Not found"})
    else:
        return data_json


if __name__ == '__main__':
    app.run(debug=True)