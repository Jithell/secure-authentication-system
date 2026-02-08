import sqlite3
import auth
from datetime import datetime

connection = sqlite3.connect(r"C:\Users\jenso\Desktop\security project\database\database.db")
cursor = connection.cursor()

def checkIfUserExists(username):
    sql = "SELECT * FROM auth WHERE username = ?"
    cursor.execute(sql, (username,))
    return cursor.fetchone() is not None


def createNewUser(user,pass_hash, salt):
    vals = (user, pass_hash, salt)
    sql = "INSERT INTO auth(username, password_hash, salt) VALUES(?,?,?)"
    cursor.execute(sql, vals)
    connection.commit()


def viewNotes(ID):
    sql = "SELECT * FROM data WHERE user_id = ?"
    cursor.execute(sql, (ID,))
    notes = cursor.fetchall()
    for k in notes:
        data_id = k[0]
        encrypted_note = k[2]
        timestamp = k[3]

        note = auth.decryptNote(encrypted_note)
        print(f"ID: {data_id} TIMESTAMP: {timestamp} NOTE: {note}")


def makeNote(ID, note):
    vals = (ID, auth.encryptNote(note), datetime.now())
    sql = "INSERT INTO data(user_id, encrypted_note, timestamp) VALUES(?,?,?)"
    cursor.execute(sql, vals)
    connection.commit()


def deleteNote(noteID, userID):
    sql = "DELETE FROM data WHERE data_id = ? AND user_id = ?"
    cursor.execute(sql, (noteID, userID))
    connection.commit()


def loginAttemptLog(username, result, reason):
    vals = (username, datetime.now(), result, reason)
    sql = "INSERT INTO attempts(username, timestamp, result, reason) VALUES(?,?,?,?)"
    cursor.execute(sql, vals)
    connection.commit()


def getID(username):
    sql = "SELECT user_id FROM auth WHERE username = ?"
    cursor.execute(sql, (username,))
    ID = cursor.fetchone()
    return ID[0] if ID else None

def getSalt(username):
    sql = "SELECT salt FROM auth WHERE username = ?"
    cursor.execute(sql, (username,))
    salt = cursor.fetchone()
    return salt[0] if salt else None


def getHashedPass(username):
    sql = "SELECT password_hash FROM auth WHERE username = ?"
    cursor.execute(sql, (username,))
    hashedPass = cursor.fetchone()
    return hashedPass[0] if hashedPass else None
