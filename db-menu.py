import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()

def getConnection():
    connection = mysql.connector.connect(
        host=os.getenv('SQL_HOST'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PWD'),
        db=os.getenv('SQL_DB')
    )
    return connection

def printTable():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("select * from CrewMember")
    myresult = cursor.fetchone()
    
    print("In the CrewMember table, we have the following items: ")
    while myresult is not None:
        print(myresult)
        myresult = cursor.fetchone()
    connection.close()
    print()

def insertIntoTable():
    firstname = input("Please give the first name of the crew member: ")
    lastname = input("Please give the last name of the crew member: ")
    email = input("Please give the email of the crew member: ")
    role = input("Please give the role of the crew member: ")
    connection = getConnection()
    cursor = connection.cursor()
    query = "insert into CrewMember (first_name, last_name, email, role) values (%s, %s, %s, %s);"
    cursor.execute(query, (firstname, lastname, email, role))
    connection.commit()
    connection.close()

def deleteRowFromTable():
    rowToDelete = input("What is the id of the row to delete? ")
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("delete from CrewMember where crewmember_id=%s", (rowToDelete,))
    connection.commit()
    connection.close()

def updateRow():
    rowToUpdate = input("What is the id of the row you want to update? ")
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("select * from CrewMember where crewmember_id=%s", (rowToUpdate,))
    myResult = cursor.fetchone()
    print(f"The current row has the value: {myResult}")
    firstname = input("Please give the first name of the crew member: ")
    lastname = input("Please give the last name of the crew member: ")
    email = input("Please give the email of the crew member: ")
    role = input("Please give the role of the crew member: ")
    cursor.execute("update CrewMember set first_name=%s, last_name=%s, email=%s, role=%s where crewmember_id=%s", (firstname, lastname, email, role, rowToUpdate))
    connection.commit()
    connection.close()


menuText = """Please select one of the following options:
1) Display contents of table
2) Insert new row to table
3) Update a row of the table
4) Delete a row of the table
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            printTable()
        elif menuOption == "2":
            insertIntoTable()
        elif menuOption == "3":
            updateRow()
        elif menuOption == "4":
            deleteRowFromTable()