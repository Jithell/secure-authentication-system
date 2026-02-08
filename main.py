import auth
import databaseHandler
from datetime import datetime, timedelta

maxAttempts = 5
lockoutSecs = 360

def isUserLocked(username):
    sql = "SELECT timestamp FROM attempts WHERE username = ? AND result = 'DENIED' ORDER BY timestamp DESC LIMIT ?"
    databaseHandler.cursor.execute(sql, (username, maxAttempts))
    rows = databaseHandler.cursor.fetchall()

    if len(rows) < maxAttempts:
        return False
    else:
        latestAttempt = datetime.strptime(rows[0][0], "%Y-%m-%d %H:%M:%S.%f")
        lockoutUntil = latestAttempt + timedelta(seconds=lockoutSecs)
        return datetime.now() < lockoutUntil


while True:
    selected_option = input("select one of the following 'log in', 'create account', 'exit'")

    if selected_option.lower() == "create account":
        while True:
            username = input("CREATE USERNAME: ")
            usernameExists = databaseHandler.checkIfUserExists(username)

            if usernameExists:
                print("Username taken, please create a new username")
                continue

            while True:
                unhashedPassword = input("CREATE PASSWORD: ")
                confirmPassword = input("CONFIRM PASSWORD: ")

                if unhashedPassword != confirmPassword:
                    print("Passwords did not match")
                    continue

                if unhashedPassword == confirmPassword:
                    salt, pass_hash = auth.hashPassword(unhashedPassword)
                    databaseHandler.createNewUser(username, pass_hash, salt)
                    print("Account created!")
                    break

            break


    if selected_option.lower() == "log in":
        while True:
            username = input("ENTER USERNAME: ")

            if isUserLocked(username):
                print("Too many attempts, try again later")
                continue

            password = input("ENTER PASSWORD: ")

            usernameExists = databaseHandler.checkIfUserExists(username)

            if usernameExists:
                salt = databaseHandler.getSalt(username)
                storedHash = databaseHandler.getHashedPass(username)
                passwordCorrect = auth.checkPassword(salt, storedHash, password)
            else:
                passwordCorrect = False

            if not (usernameExists and passwordCorrect):
                databaseHandler.loginAttemptLog(username, "DENIED", "Incorrect credentials")
                print("Incorrect credentials!")
            else:
                databaseHandler.loginAttemptLog(username, "SUCCESS", "Login successful")
                print(f"Logged in as {username}!")
                while True:
                    choice = input("select one of the following 'View Notes', 'Delete Note', 'Create Note', 'logout'")

                    if choice.lower() == "view notes":
                        databaseHandler.viewNotes(databaseHandler.getID(username)) 

                    if choice.lower() == "delete note":
                        noteID = int(input("ENTER NOTE ID TO BE DELETED: "))
                        databaseHandler.deleteNote(noteID, databaseHandler.getID(username))

                    if choice.lower() == "create note":
                        note = input("ENTER NOTE: ")
                        databaseHandler.makeNote(databaseHandler.getID(username), note)

                    if choice.lower() == "logout":
                        print("logged out!")
                        break
                break

    if selected_option.lower() == "exit":
        break