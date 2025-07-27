from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
import json
import os
import base64

'''

'''
DATA_FILE = "pw.json"
SALT_FILE = "salt.bin"
VAULT_FILE = "vault.enc"

def deriveKey(password:str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length = 32,
        salt=salt,
        iterations= 100000
        )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def loadSalt(saltPath = SALT_FILE):
    if os.path.exists(saltPath):
        with open(saltPath, "rb") as f:
            return f.read()
    else:
        salt = os.urandom(16)
        with open(saltPath, "wb") as f:
            f.write(salt)
        return salt

def nonEmpty(fieldName: str):
    while True:
        value = input(f"Enter {fieldName} (or input \":q\" to cancel): ").strip()
        if value.lower() == ":q":
            print("Operation Canceled")
            return None
        if value:
            return value
            
        print(f"{fieldName} can not be empty.")

# TODO: issue found where if there is no vault and salt, then it treats it as a first start up.
# Clarification on intended behaviour required. If the user does not store a password is there a point to keeping the master password?
# saveData line can be removed.
def loadData(vaultPath = VAULT_FILE, saltPath = SALT_FILE):
    print("If there is no vault, you may create one by entering a master password and adding a record.\n")
    masterPw = nonEmpty("Master Password").strip()
    salt = loadSalt(saltPath)
    key = deriveKey(masterPw, salt)
    fernet = Fernet(key)

    if not os.path.exists(vaultPath):
        saveData({},fernet)
        return {}, fernet
    try:
        with open(vaultPath, "rb") as file:
            encrypted = file.read()
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted), fernet
    except InvalidToken:
        print("Incorrect master password or corrupted vault.")
        exit(1)

def saveData(data, fernet, vaultPath = VAULT_FILE):
    jsonData = json.dumps(data).encode()
    encrypted = fernet.encrypt(jsonData)
    with open(vaultPath, "wb") as f:
        f.write(encrypted)

def addPw(data, fernet):
    site = nonEmpty("Site Name")
    if not site:
        return
    
    if site in data:
        print(f"Entry for {site} seems to already exist. Use \"update password\" to modify it.")
        return
    print(site)
    username = nonEmpty("Username")
    if not username:
        return
    password = nonEmpty("Password")
    if not password:
        return
    
    data[site] = {"username": username, "password": password}
    saveData(data, fernet)
    print(f"Saved entry for {site}.")

def getPw(data):
    site = nonEmpty("Site name")
    if not site:
        return
    entry = data.get(site)
    if entry:
        print(f"Username = {entry['username']}")
        print(f"Password = {entry['password']}")
    else:
        print(f"No entry found for {site}.")

def listSites(data):
    if not data:
        print("No Entries availible")
    else:
        print("Saved Sites:")
        for site in data:
            print(f"- {site}")  

def updatePw(data, fernet):
    site = nonEmpty("Site name")
    if not site:
        return
    entry = data.get(site)
    if entry:
        print(f"Username = {entry['username']}")
        print(f"Current password = {entry['password']}")
        newPassword = input("Enter new password: ")
        entry['password'] = newPassword
        saveData(data, fernet)
        print(f"Updated entry for {site}")
    else:
        print(f"No entry found for {site}.")

def removePw(data, fernet):
    site = nonEmpty("SiteName")
    if not site:
        return
    data.pop(site)
    saveData(data, fernet)
    print(f"Removed entry for {site}")

def main():
    data, fernet = loadData(VAULT_FILE, SALT_FILE)
    while True:
        print(" Operations: ")
        print("1. Add new password")
        print("2. Retrieve password")
        print("3. Update password")
        print("4. Remove entry")
        print("5. List all sites")
        print("Q. Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            addPw(data, fernet)
        elif choice == "2":
            listSites(data)
            getPw(data)
        elif choice == "3":
            updatePw(data, fernet)
        elif choice == "4":
            removePw(data, fernet)
        elif choice == "5":
            listSites(data)
        elif choice.lower() == "q":
            print("Farewell")
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()