import mysql
import mysql.connector

db = None
handler = None

connected = False

frame = 2
recogs = 1
errors = 1

class Database:

    @staticmethod
    def connect(host = "localhost", user = "root", password = "root", dbName = "pinpoint"):
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
                Database.sendQuery("SET FOREIGN_KEY_CHECKS=0;")
                Database.sendQuery("TRUNCATE TABLE position")
                Database.sendQuery("TRUNCATE TABLE recognitions")
                Database.sendQuery("TRUNCATE TABLE errors")
                #Database.sendQuery("SET FOREIGN_KEY_CHECKS=1;")
                return ("Connection to " + dbName + " was estabilished.")
            else:
                return ("You are already connected to: " + dbName)
        except:
            return "Connecting to " + dbName + " was unsuccesfull, is the server up and running, are the paramaters correct?"

    @staticmethod
    def logPos(pos):
        global handler
        global connected
        global frame

        if(not connected):
            return "You are not connected to the database, queries can't be executed without connection."
        handler.execute("INSERT INTO position (id, pos) VALUES (%s, %s)", (frame, str(pos)))
        frame += 1
        db.commit()

    @staticmethod
    def logRecogs():
        global handler
        global connected
        global recogs

        if(not connected):
            return "You are not connected to the database, queries can't be executed without connection."
        handler.execute("INSERT INTO recognitions (recID) VALUES (" + str(recogs) + ")")
        recogs += 1
        db.commit()

    @staticmethod
    def logError(eType):
        global handler
        global connected
        global errors

        if(not connected):
            return "You are not connected to the database, queries can't be executed without connection."
        handler.execute("INSERT INTO errors (errorId, error_type) VALUES (%s, %s)", (errors, eType))
        errors += 1
        db.commit()

    @staticmethod
    def sendQuery(query):
        global handler
        global connected

        if(not connected):
            return "You are not connected to the database, queries can't be executed without connection."
        handler.execute(query)
        db.commit()

    def getRecogsNums():
        global recogs
        return recogs

    @staticmethod
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
