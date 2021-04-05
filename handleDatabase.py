import mysql
import mysql.connector

db = None
handler = None 

#FBX python -> Unity Animation

connected = False

def connect(host = "localhost", user = "root", password = "", dbName = "pinpoint"):
    global db
    try:
        if(db == None):
            db = mysql.connector.connect(
                host= host,
                user= user,
                passwd= password,
                database= dbName
            )

            global connected
            if(db.is_connected()):
                connected = True

            global handler
            handler = db.cursor()
            return ("Connection to " + dbName + " was estabilished.")
        else:
            return ("You are already connected to: " + dbName)
    except:
        return "Connecting to " + dbName + " was unsuccesfull, is the server up and running, are the paramaters correct?"

def logError(recognitionID, errorType):
    pass

def sendQuery(query):
    global handler
    global connected

    if(not connected):
        return "You are not connected to the database, queries can't be executed without connection."
    handler.execute(query)

def disconnect():
    global handler
    global db

    handler.close()
    db.disconnect()
    if(not db.is_connected()):
        return "Succesfully disconnected from database."
    else: 
        return "Disconnecting from database was unsuccesfull."

def __init__(self):
    return "Succesfully created Database Handler"
