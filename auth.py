import hashlib
import os
from cryptography.fernet import Fernet

with open(r"C:\Users\jenso\Desktop\security project\key.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)
attempts = 0


def hashPassword(password):
    salt = os.urandom(16)
    hashed_pass = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_420
    )
    return salt, hashed_pass


def checkPassword(salt, hashed_pass, inputted_password):
    newHashed_password = hashlib.pbkdf2_hmac(
        "sha256",
        inputted_password.encode(),
        salt,
        100_420
    )
    return hashed_pass == newHashed_password


def encryptNote(note):
    return cipher.encrypt(note.encode())


def decryptNote(note):
    return cipher.decrypt(note).decode()


#TEST ENCRYPTION WORKS
# test = input("INPUT NOTE: ")

# testencrypted = encryptNote(test)
# print(f"ENCRYPTED: {testencrypted}")

# testdecrypted = decryptNote(testencrypted)
# print(f"DECRYPTED: {testdecrypted}")