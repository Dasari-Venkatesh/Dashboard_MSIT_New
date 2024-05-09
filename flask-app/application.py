import io
import sys
sys.path.append('C:/Python39/Lib/site-packages')

from flask import Flask, render_template, jsonify, request

from flask_cors import CORS
import csv, json
import pandas as pd
from collections import OrderedDict 
from collections import defaultdict
from utils import get_data_from_excel
import datetime

from utils import user_exists, send_email

app = Flask(__name__)
cors = CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/get_scores/*": {"origins": "http://localhost:3000"}
})


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


@app.route("/get_scores/<string:student_email>")
def get_scores(student_email):
    values = get_data_from_excel('scores')
    headers = values[0]
    json_str = None
    for row in values[1:]:
        if row[1] == student_email:
            row_dict = dict(zip(headers, row))
            json_str = json.dumps(row_dict, indent=4)
    if json_str:
        return json_str
    return jsonify({'message': "Email Not found"})



@app.route('/add-user/', methods=['POST'])
def add_user():
    user_details = request.get_json()

    username = user_details['username']
    email = user_details['email']

    if user_exists(email):
        return jsonify({'message': 'User details already exists'})

    with open('./users/users.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([email, username])
    send_email(email, username)
    return jsonify({'message': 'User details stored successfully'}), 201


@app.route('/add-users/', methods=['POST'])
def add_users():
    if 'file' not in request.files:
        return jsonify({'message':'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    if file and file.filename.endswith('.csv'):
        try:
            with open('./users/users.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_file = io.TextIOWrapper(file, encoding='utf-8')
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if not user_exists(row[0]):
                        csv_writer.writerow(row)
                        
            return jsonify({'message': 'Users details stored successfully'}), 201

        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'})
    else:
        return jsonify({'message': 'Invalid file format. Please upload a CSV file.'})


@app.route('/search-emails', methods=['GET'])
def search_emails():
    query_param = request.args.get('query')
    with open('users.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        emails = [row['email'] for row in csv_reader]

    suggestions = [email for email in emails if query_param in email]

    return jsonify({'emails': suggestions})


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


if __name__ == '__main__':
    app.run(debug=True)