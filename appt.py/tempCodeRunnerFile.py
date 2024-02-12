from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, methods=['GET', 'POST'])  # Allow both GET and POST requests

# MySQL Configuration (replace with your actual values)
db_config = {
    'host': '127.0.0.1',  
    'port': 3306,         
    'user': 'root',
    'password': '12345',
    'database': 'attendance_system',
}


 #MySQL connection
db = pymysql.connect(**db_config)
cursor = db.cursor()

# Mark Attendance Route
@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    try:
        data = request.get_json()
        student_id = data['student_id']
        status = data['status']
        date = '2023-12-01'  

       
        print(f"Received request to mark attendance - Student ID: {student_id}, Status: {status}")

        #  MySQL code to insert attendance record 
        sql = 'INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)'
        cursor.execute(sql, (student_id, date, status))
        db.commit()

        return 'Attendance marked successfully'
    except Exception as e:
        # Log error to the console
        print("Error marking attendance:", str(e))
        return 'Error marking attendance'

# View Attendance Route
@app.route('/view-attendance', methods=['GET'])
def view_attendance():
    student_id = request.args.get('student_id')

    # Your SQL code to retrieve attendance records based on the student ID
    sql = 'SELECT date, status FROM attendance WHERE student_id = %s'
    cursor.execute(sql, (student_id,))
    attendance_records = cursor.fetchall()

    # Convert the result to a list of dictionaries for JSON response
    result = [{'date': record[0], 'status': record[1]} for record in attendance_records]

    return jsonify(result)

# Existing __main__ block
if __name__ == '__main__':
    app.run(debug=True)
