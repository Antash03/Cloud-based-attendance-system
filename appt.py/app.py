from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pymysql
from datetime import date

app = Flask(__name__)
CORS(app, methods=['GET', 'POST'])  

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '12345',
    'database': 'attendance_system',
}

db = pymysql.connect(**db_config)
cursor = db.cursor()

@app.route('/')
def main_page():
    return render_template('att0.html')  

@app.route('/teacher-login')
def teacher_login_page():
    return render_template('att1.html')  

@app.route('/teacher-dashboard')
def teacher_dashboard():
    return render_template('att2.html')  


@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    try:
        data = request.get_json()
        student_id = data['student_id']
        status = data['status']

        
        current_date = date.today().strftime('%Y-%m-%d')

        print(f"Received request to mark attendance - Student ID: {student_id}, Status: {status}, Date: {current_date}")

        
        sql = 'INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)'
        cursor.execute(sql, (student_id, current_date, status))
        db.commit()

        return 'Attendance marked successfully'
    except Exception as e:
        
        print("Error marking attendance:", str(e))
        return 'Error marking attendance'


@app.route('/view-attendance', methods=['GET'])
def view_attendance():
    student_id = request.args.get('student_id')

    
    sql = 'SELECT date, status FROM attendance WHERE student_id = %s'
    cursor.execute(sql, (student_id,))
    attendance_records = cursor.fetchall()

    result = [{'date': record[0], 'status': record[1]} for record in attendance_records]

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
