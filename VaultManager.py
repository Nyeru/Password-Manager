from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
import json
import os
import base64

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


class VaultManager:
    def __init__(self, vaultPath=VAULT_FILE, saltPath = SALT_FILE):
        self.vaultPath = VAULT_FILE
        self.saltPath = SALT_FILE
        self.data = {}
        self.fernet = None
    
    def loadVault(self, masterPass: str) -> bool:
        salt = loadSalt(self.saltPath)
        key = deriveKey(masterPass, salt)
        self.fernet = Fernet(key)

        if not os.path.exists(self.vaultPath):
            self.data = {}
            self.saveVault()
            return True
        try:
            with open(self.vaultPath, "rb") as file:            
                decrypted = self.fernet.decrypt(file.read())
            self.data = json.loads(decrypted)
            return True
        except InvalidToken:
            return False
    
    def saveVault(self):
        data = json.dumps(self.data)
        encrypted = self.fernet.encrypt(data.encode())
        with open(self.vaultPath, "wb") as f:
            f.write(encrypted)
    
    def createRecord(self, site, username, password):
        self.data[site] = {"username": username, "password": password}
        self.saveVault()

    def retrieveRecord(self, site: str):
        return self.data.get(site)
    
    def updateRecord(self, site: str, password:str):
        if site in self.data:
            self.data[site]["password"] = password
            self.saveVault()

    def deleteRecord(self, site: str):
        if site in self.data:
            del self.data[site] 
            self.saveVault()
    
    def listSites(self):
        return list(self.data.keys())
    
    def recordExists(self, site:str):
        return site in self.data.keys()