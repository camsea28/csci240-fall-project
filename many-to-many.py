import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()

## done
def getConnection():
    connection = mysql.connector.connect(
        host=os.getenv('SQL_HOST'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PWD'),
        db=os.getenv('SQL_DB')
    )
    return connection

## done
def printCrewMembers():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select * from CrewMember")
    myResult = myCursor.fetchone()

    print("In the CrewMember table, we have the following team members: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()

## done
def printEvents():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select event_id, name from Event")
    myResult = myCursor.fetchone()

    print("In the Event table, we have the following events: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()

## done
def printEventsForCrewMember():
    connection = getConnection()
    myCursor = connection.cursor()
    crewmember_id = input("For which crewmember_id would you like to view the events? ")
    myCursor.execute("select e.event_id, name from Event as e join CrewMember_Event on e.event_id=CrewMember_Event.event_id where crewmember_id=%s", (crewmember_id,))
    myResult = myCursor.fetchall()
    print(f"This crew member are {len(myResult)} events: ")
    for row in myResult:
        print(row)
    connection.close()

## done
def printCrewMembersForEvent():
    connection = getConnection()
    myCursor = connection.cursor()
    event_id = str(input("For which event_id would you like to view the crew members? "))
    myCursor.execute("select c.crewmember_id, c.first_name, c.last_name from CrewMember as c join CrewMember_Event on c.crewmember_id=CrewMember_Event.crewmember_id where event_id=%s", (event_id,))
    myResult = myCursor.fetchall()
    print(f"There are {len(myResult)} crew members assigned to this event: ")
    for row in myResult:
        print(row)
    connection.close()

## done
def addCrewMemberToEvent():
    connection = getConnection()
    myCursor = connection.cursor()
    crewmember_id = input("Enter the crewmember_id to add: ")
    event_id = input("Enter the event_id to add the crew member to: ")
    myCursor.execute("insert into CrewMember_Event (crewmember_id, event_id) values (%s, %s)", (crewmember_id, event_id))
    connection.commit()
    connection.close()

## done
def removeCrewMemberFromEvent():
    connection = getConnection()
    myCursor = connection.cursor()
    crewmember_id = input("Enter the crewmember_id to remove: ")
    event_id = input("Enter the event_id to remove the crew member from: ")
    myCursor.execute("delete from CrewMember_Event where crewmember_id=%s and event_id=%s", (crewmember_id, event_id))
    connection.commit()
    connection.close()

menuText = """Please select one of the following options:
1) Print Crew Members
2) Print Events
3) Print Events a Crew member appears in
4) Print Crew members in an Event
5) Add a Crew member to an Event
6) Remove a Crew member from an Event
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            printCrewMembers()
        elif menuOption == "2":
            printEvents()
        elif menuOption == "3":
            printEventsForCrewMember()
        elif menuOption == "4":
            printCrewMembersForEvent()
        elif menuOption == "5":
            addCrewMemberToEvent()
        elif menuOption == "6":
            removeCrewMemberFromEvent()