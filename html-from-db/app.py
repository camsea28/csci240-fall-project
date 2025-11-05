from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv('SQL_HOST'),
    user=os.getenv('SQL_USER'),
    password=os.getenv('SQL_PWD'),
    database=os.getenv('SQL_DB')
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("select * from CrewMember;")
    CrewMembers = cursor.fetchall()
    return render_template('index.html', CrewMembers=CrewMembers)

@app.route('/add', methods=['POST'])
def add_member():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    role = request.form['role']
    email = request.form['email']
    cursor.execute("insert into CrewMember (first_name, last_name, role, email) values (%s, %s, %s, %s);",
                   (first_name, last_name, role, email))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
