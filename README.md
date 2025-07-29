# Password Manager - Educational Project for some idea on encryption and security regarding password managers.

## ⚠️ Security Disclaimer

This project is a personal, local password manager designed for learning purposes or low-risk usage.
This project:
- Has not undergone offical or formal security review
- Does not implement advanced hardening (secure memory, sandboxing, anti-debugging, etc.)
- Offers no built-in backup, sync, or multi-factor authentication

**Use it at your own discretion. Do not store critical secrets or enterprise credentials.**

## Instructions
Create a venv and install requirements with
```
py -m venv .venv or python -m venv .venv
.venv/Scripts/activate  or source .venv/bin/activate
pip install -r requirements.txt  
```

Run cli.py, main.py should be functionally the same and compatabile but doesnt make use of the VaultManager class

Without an existing vault.enc, the user is able to define the master password used to access the vault.
Once inputted, there will be a list of operations to select from:
1. Adding a new record
2. Retrieving a record
3. Updating a record
4. Removing a record
5. Listing all records
6. Exiting

**If the master password is forgotten or lost, there is no salvaging it. Delete the vault.enc or/and the salt.bin and rerun the script to set up a new master password.**

# Phase 1: CLI Password Manager
Functional Requirements
   - Each record is identified by the site (Unique Identifier)
   - Records include: Site Name, username, password
   Users are able to:
      - Add a record
      - Retrieve a record
      - Update the password in a record
      - Retrieve a list of all sites stored
      - Remove a record
   Password Manager should:
      - Validate user input 
         - Inputs must be nonempty
      - Handle File Errors 

At this stage, the password manager  features 0 security and is merely an interface for a password json.

# Phase 2: Master password + Encryption
   - Concepts to look at:
      - **Hashing**
         - Typically, passwords are hashed and then stored. However, hashing is a one way operation and in a password manager, users would like to view the unhashed passwords for use, thus they will not be hashed before storing.
         - Storing passwords in hash is typically more secure as there is no way to decrypt passwords and it allows for 
      - **Encryption**
         - Encryption involves scrambling the readable, plaintext data  into ciphertext using some sort of algorithm.
         - Encryption algorithms are done using secret keys which also facilitate the decryption of the ciphertext. There are two types of encryption: symmetric where the key is used for both encryption and decryption and asymmetric where there is a seperate key for each process.
         Symmetrics share the same encryption/decryption key and is faster, however with a single key for both it is slightly less secure than asymmetric methods.
      - **Salting**
         - Salting a password involves adding a unique randomly generated string or set of bytes to a password before encrypting or hashing. In broader applications, salts are unique for each user, and this has the benefit of slowing down the attacker as the hashes need to be cracked one by one.
         - It is also an extra bit of security when two users have the same passwords, their hashes will be completely different. Salting should be highly effective against precomupted attempts to crack passwords.
   - Functional Requirements 
      - Ask for a master password
      - Exit if incorrect password, allow access if not
         - Possible registration feature and account system?
         - Multiple users would be far future, this is local and should only have a single user.
         - User defined master password, 
      - Derive key from master password for use in encryption/decryption of entries
         - Key derivation using PBKDF2HMAC
         - Fernet to encrypt/decrypt the json.
         - Store the encrypted data in a vault file (vault.enc)
         - Store salt in a bin file
      - Store salt in Salt.bin
      - Store encrypted data in vault.enc
      - Decrypt vault.enc after correct master password is given

**Current design and thoughts**:
   - AES Encryption using Fernet
   - PBKDF2 key derivation w salt
   - Encrypted vault file, decypted is stored in memory as a python dict.
   - Forgetting master password > hard reset of program (purge everything!)
         - No method to reset master password (Introduces weakness, angle of attack)
         - Vault is accessible and encrypted and the only method to get key would be master password. File is ddecrypted only during active session.
         - Exactly how do we allow a hard reset? Attackers can abuse it to delete the passwords if given remote access and hard reset function is easily triggered.
            - Should there be a backup within X hrs for restoration?
   - Hard reset is generally done by manually deleting the vault
      
**Vulnerabilities**:
   - Situation: Local Password manager, Assume attacker has access to machine either in person or remote
   - main concern is the python dict in memory
      - Possible memory dumping/modification of code to print out information post decryption
         - Assumes attacker has access to system state DURING runtime
         - compromised system already
            - Mitigation: Run password Manager on provate machines, Secure environment to prevent remote root or physical access
   - Other scenarios include: Attacker has the key (Compromised system already) or Attacker has read only access (Can not access/decrypt without the master password)
         
Phase 3: GUI (tkinter)
Phase 4: Extra
