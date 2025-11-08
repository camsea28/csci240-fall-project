import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import dotenv

dotenv.load_dotenv()

connection = mysql.connector.connect(
    user=os.getenv('SQL_USER'),
    password=os.getenv('SQL_PWD'),
    host=os.getenv('SQL_HOST'),
    database=os.getenv('SQL_DB')
)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def showCrewMembers():
    cursor = connection.cursor()

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    role = request.args.get('role')
    if first_name is not None and last_name is not None and email is not None and role is not None:
        cursor.execute("INSERT into CrewMember (first_name, last_name, email, role) values (%s, %s, %s, %s)", (first_name, last_name, email, role))
        connection.commit()
    elif request.args.get('delete') == 'true':
        delete_id = request.args.get('id')
        cursor.execute("DELETE from CrewMember where crewmember_id=%s", (delete_id,))
        connection.commit()

    cursor.execute("Select * from CrewMember")
    result = cursor.fetchall()
    cursor.close()
    return render_template('crewmember-list.html', collection=result)

@app.route("/updateCrewMember")
def updateCrewMember():
    id = request.args.get('id')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    role = request.args.get('role')

    if id is None:
        return "A crew member ID is required."
    elif first_name is not None and last_name is not None and email is not None and role is not None:
        cursor = connection.cursor()
        cursor.execute("UPDATE CrewMember set first_name=%s, last_name=%s, email=%s, role=%s where crewmember_id=%s", (first_name, last_name, email, role, id))
        cursor.close()
        connection.commit()
        return redirect(url_for('showCrewMembers'))

    cursor = connection.cursor()
    cursor.execute("select first_name, last_name, email, role from CrewMember where crewmember_id=%s;", (id,))
    existing_first, existing_last, existing_email, existing_role = cursor.fetchone()
    cursor.close()
    return render_template('crewmember-update.html', id=id, existingFirst=existing_first, existingLast=existing_last, existingEmail=existing_email, existingRole=existing_role)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")