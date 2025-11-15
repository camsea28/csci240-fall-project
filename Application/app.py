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
def index():
    return render_template('index.html')

@app.route('/showcrewmembers', methods=['GET'])
def show_crewmembers():
    # noinspection DuplicatedCode
    cursor = connection.cursor()
    event_id = request.args.get('event_id')
    if request.args.get('unassign') == 'true':
        crewmember_id = request.args.get('crewmember_id')
        if event_id is not None and crewmember_id is not None:
            cursor.execute("DELETE FROM CrewMember_Event WHERE crewmember_id=%s AND event_id=%s", (crewmember_id, event_id))
            connection.commit()

    if event_id is not None:
        cursor.execute("""SELECT cm.crewmember_id, cm.first_name, cm.last_name, e.name, e.location from CrewMember as cm
            JOIN CrewMember_Event as cme ON cm.crewmember_id = cme.crewmember_id
            JOIN Event as e ON cme.event_id = e.event_id
            WHERE e.event_id=%s"""
                       , (event_id,))
        result = cursor.fetchall()
        if len(result) >= 1:
            event_name = result[0][3]
            event_number = result[0][4]
        else:
            event_name = event_number = "Unknown"
        page_title = f"{event_name} ({event_number}) Team"
    else:
        cursor.execute("SELECT crewmember_id, first_name, last_name from CrewMember")
        page_title = "Crew members"
        result = cursor.fetchall()

    cursor.close()
    return render_template('crewmembers.html', crewmembers=result, pageTitle=page_title, event_id=event_id)

@app.route('/showevents', methods=['GET'])
def show_events():
    # noinspection DuplicatedCode
    cursor = connection.cursor()

    crewmember_id = request.args.get('crewmember_id')
    if request.args.get('unassign') == 'true':
        event_id = request.args.get('event_id')
        if event_id is not None and crewmember_id is not None:
            cursor.execute("DELETE FROM CrewMember_Event WHERE crewmember_id=%s AND event_id=%s", (crewmember_id, event_id))
            connection.commit()


    if crewmember_id is not None:
        assign_event_id = request.args.get('assign_event_id')
        if assign_event_id is not None:
            cursor.execute("INSERT INTO CrewMember_Event (crewmember_id, event_id) VALUES (%s, %s)", (crewmember_id, assign_event_id))
            connection.commit()

        cursor.execute("SELECT first_name, last_name FROM CrewMember WHERE crewmember_id=%s", (crewmember_id,))
        crew_name_result = cursor.fetchone()
        if crew_name_result:
            crewmember_name = crew_name_result[0] + " " + crew_name_result[1]
        else:
            crewmember_name = "Unknown"

        cursor.execute("""SELECT e.event_id, e.name, cm.first_name, cm.last_name from Event as e
            JOIN CrewMember_Event as cme ON e.event_id = cme.event_id
            JOIN CrewMember as cm ON cm.crewmember_id = cme.crewmember_id
            WHERE cm.crewmember_id=%s"""
                    , (crewmember_id,))
        result = cursor.fetchall()

        cursor.execute(
            """SELECT event_id, name, location FROM Event
                WHERE event_id NOT IN (
                    SELECT event_id FROM CrewMember_Event WHERE crewmember_id=%s
                )""",
            (crewmember_id,)
        )
        other_events = cursor.fetchall()
        page_title = f"Events assigned to {crewmember_name}:"
    else:
        cursor.execute("SELECT event_id, name, location from Event")
        page_title = "Showing all events"
        result = cursor.fetchall()
        other_events = None

    cursor.close()
    return render_template('events.html', crewmember_id=crewmember_id, event_list=result, other_events=other_events, pageTitle=page_title)

@app.route('/manageCrewmembers', methods=['GET'])
def manage_crewmembers():
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
def update_crewmember():
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
        return redirect(url_for('manage_crewmembers'))

    cursor = connection.cursor()
    cursor.execute("select first_name, last_name, email, role from CrewMember where crewmember_id=%s;", (id,))
    existing_first, existing_last, existing_email, existing_role = cursor.fetchone()
    cursor.close()
    return render_template('crewmember-update.html', id=id, existingFirst=existing_first, existingLast=existing_last, existingEmail=existing_email, existingRole=existing_role)



if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")