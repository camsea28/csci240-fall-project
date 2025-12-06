import os
import re
from datetime import datetime
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
    error = None

    event_id = request.args.get('event_id')
    if event_id:
        if not validate_integer(event_id):
            error = "Invalid Event ID provided."
            event_id = None

    if request.args.get('unassign') == 'true':
        crewmember_id = request.args.get('crewmember_id')
        if event_id and crewmember_id:
            if not validate_integer(crewmember_id):
                error = "Invalid Crew Member ID for unassignment."
            else:
                cursor.execute("DELETE FROM CrewMember_Event WHERE crewmember_id=%s AND event_id=%s", (crewmember_id, event_id))
                connection.commit()

    if event_id:
        assign_crewmember_id = request.args.get('assign_crewmember_id')
        if assign_crewmember_id:
            if not validate_integer(assign_crewmember_id):
                error = "Invalid Crew Member ID for assignment."
            else:
                cursor.execute("INSERT INTO CrewMember_Event (crewmember_id, event_id) VALUES (%s, %s)", (assign_crewmember_id, event_id))
                connection.commit()

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
            cursor.execute("SELECT name, location FROM Event WHERE event_id=%s", (event_id,))
            event_info = cursor.fetchone()
            if event_info:
                event_name = event_info[0]
                event_number = event_info[1]
            else:
                event_name = event_number = "Unknown"

        cursor.execute(
            """SELECT crewmember_id, first_name, last_name, role FROM CrewMember
                WHERE crewmember_id NOT IN (
                    SELECT crewmember_id FROM CrewMember_Event WHERE event_id=%s
                )""",
            (event_id,)
        )
        other_crewmembers = cursor.fetchall()
        page_title = f"{event_name} ({event_number}) Team"
    else:
        cursor.execute("SELECT crewmember_id, first_name, last_name from CrewMember")
        page_title = "Crew members"
        result = cursor.fetchall()
        other_crewmembers = None

    cursor.close()
    return render_template('crewmembers.html', crewmembers=result, pageTitle=page_title, event_id=event_id, other_crewmembers=other_crewmembers, error=error)

@app.route('/showevents', methods=['GET'])
def show_events():
    # noinspection DuplicatedCode
    cursor = connection.cursor()
    error = None

    crewmember_id = request.args.get('crewmember_id')
    if crewmember_id:
        if not validate_integer(crewmember_id):
            error = "Invalid Crew Member ID provided."
            crewmember_id = None

    if request.args.get('unassign') == 'true':
        event_id = request.args.get('event_id')
        if crewmember_id and event_id:
            if not validate_integer(event_id):
                error = "Invalid Event ID for unassignment."
            else:
                cursor.execute("DELETE FROM CrewMember_Event WHERE crewmember_id=%s AND event_id=%s", (crewmember_id, event_id))
                connection.commit()


    if crewmember_id:
        assign_event_id = request.args.get('assign_event_id')
        if assign_event_id:
            if not validate_integer(assign_event_id):
                error = "Invalid Event ID for assignment."
            else:
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
    return render_template('events.html', crewmember_id=crewmember_id, event_list=result, other_events=other_events, pageTitle=page_title, error=error)

@app.route('/manageCrewmembers', methods=['GET'])
def manage_crewmembers():
    cursor = connection.cursor()
    error = None

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    role = request.args.get('role')

    if first_name and last_name and email and role:
        if not first_name.strip():
            error = "First name cannot be empty."
        elif not last_name.strip():
            error = "Last name cannot be empty."
        elif not validate_email(email):
            error = "Invalid email format."
        elif not role.strip():
            error = "Role cannot be empty."
        if not error:
            cursor.execute("INSERT into CrewMember (first_name, last_name, email, role) values (%s, %s, %s, %s)", (first_name, last_name, email, role))
            connection.commit()
            return redirect(url_for('manage_crewmembers'))
    elif request.args.get('delete') == 'true':
        delete_id = request.args.get('id')
        if not validate_integer(delete_id):
            error = "Invalid crew member ID for deletion."
        else:
            cursor.execute("DELETE from CrewMember where crewmember_id=%s", (delete_id,))
            connection.commit()

    cursor.execute("Select * from CrewMember")
    result = cursor.fetchall()
    cursor.close()
    return render_template('crewmember-list.html', collection=result, error=error)

@app.route("/updateCrewMember")
def update_crewmember():
    error = None
    crewmember_id = request.args.get('id')

    if not crewmember_id:
        return "A crew member ID is required."
    if not validate_integer(crewmember_id):
        return "Invalid crew member ID."

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    role = request.args.get('role')

    if first_name is not None and last_name is not None and email is not None and role is not None:
        if not first_name.strip():
            error = "First name cannot be empty."
        elif not last_name.strip():
            error = "Last name cannot be empty."
        elif not validate_email(email):
            error = "Invalid email format."
        elif not role.strip():
            error = "Role cannot be empty."

        if not error:
            cursor = connection.cursor()
            cursor.execute("UPDATE CrewMember set first_name=%s, last_name=%s, email=%s, role=%s where crewmember_id=%s", (first_name, last_name, email, role, crewmember_id))
            cursor.close()
            connection.commit()
            return redirect(url_for('manage_crewmembers'))
    
    cursor = connection.cursor()
    cursor.execute("select first_name, last_name, email, role from CrewMember where crewmember_id=%s;", (crewmember_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        existing_first, existing_last, existing_email, existing_role = result
        return render_template(
            'crewmember-update.html',
            id=crewmember_id,
            existingFirst=first_name if first_name is not None else existing_first,
            existingLast=last_name if last_name is not None else existing_last,
            existingEmail=email if email is not None else existing_email,
            existingRole=role if role is not None else existing_role,
            error=error
        )
    else:
        return redirect(url_for('manage_crewmembers', error="Crew Member not found."))

@app.route('/manageEvents', methods=['GET'])
def manage_events():
    cursor = connection.cursor()
    error = None

    name = request.args.get('name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    location = request.args.get('location')

    if name is not None and start_date is not None and end_date is not None and location is not None:
        # noinspection DuplicatedCode
        if not name.strip():
            error = "Event name cannot be empty."
        elif not validate_date(start_date):
            error = "Invalid start date format (YYYY-MM-DD)."
        elif not validate_date(end_date):
            error = "Invalid end date format (YYYY-MM-DD)."
        elif datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'):
            error = "Start date cannot be after end date."
        elif not location.strip():
            error = "Location cannot be empty."

        if not error:
            cursor.execute("INSERT into Event (name, start_date, end_date, location) values (%s, %s, %s, %s)", (name, start_date, end_date, location))
            connection.commit()
            return redirect(url_for('manage_events'))
    elif request.args.get('delete') == 'true':
        delete_id = request.args.get('id')
        if not validate_integer(delete_id):
            error = "Invalid event ID for deletion."
        else:
            cursor.execute("DELETE from Event where event_id=%s", (delete_id,))
            connection.commit()

    cursor.execute("Select * from Event")
    result = cursor.fetchall()
    cursor.close()
    return render_template('event-list.html', collection=result, error=error)

@app.route("/updateEvent")
def update_event():
    error = None
    event_id = request.args.get('id')

    if not event_id:
        return "An event ID is required."
    if not validate_integer(event_id):
        return "Invalid event ID."

    name = request.args.get('name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    location = request.args.get('location')

    if name is not None and start_date is not None and end_date is not None and location is not None:
        # noinspection DuplicatedCode
        if not name.strip():
            error = "Event name cannot be empty."
        elif not validate_date(start_date):
            error = "Invalid start date format (YYYY-MM-DD)."
        elif not validate_date(end_date):
            error = "Invalid end date format (YYYY-MM-DD)."
        elif datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'):
            error = "Start date cannot be after end date."
        elif not location.strip():
            error = "Location cannot be empty."

        if not error:
            cursor = connection.cursor()
            cursor.execute("UPDATE Event set name=%s, start_date=%s, end_date=%s, location=%s where event_id=%s", (name, start_date, end_date, location, event_id))
            cursor.close()
            connection.commit()
            return redirect(url_for('manage_events'))
    
    cursor = connection.cursor()
    cursor.execute("select name, start_date, end_date, location from Event where event_id=%s;", (event_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        existing_name, existing_start_date, existing_end_date, existing_location = result
        return render_template(
            'event-update.html',
            id=event_id,
            existingName=name if name is not None else existing_name,
            existingStartDate=start_date if start_date is not None else str(existing_start_date),
            existingEndDate=end_date if end_date is not None else str(existing_end_date),
            existingLocation=location if location is not None else existing_location,
            error=error
        )
    else:
        return redirect(url_for('manage_events', error="Event not found."))

def validate_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_integer(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")