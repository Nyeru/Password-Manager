from VaultManager import VaultManager

def promptInput(fieldName: str):
    while True:
        value = input(f"Enter {fieldName} (or input \":q\" to cancel): ").strip()
        if value.lower() == ":q":
            print("Operation Canceled")
            return None
        if value:
            return value
            
        print(f"{fieldName} can not be empty.")

def siteList(manager: VaultManager):
    sites = manager.listSites()
    if not sites:
        print("No Entries availible")
    else:
        print("Saved Sites:")
        for site in sites:
            print(f"- {site}")  

def main():
    manager = VaultManager()
    masterPw = promptInput("master password")
    if not manager.loadVault(masterPw):
        print("Wrong password or corrupted vault.")
        exit(1)
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
                site = promptInput("Site Name")
                if not site:
                    continue
                if manager.recordExists(site):
                    print(f"Entry for {site} seems to already exist. Use \"update password\" to modify it.")
                    continue
                username = promptInput("username")
                if not username:
                    continue
                password = promptInput("password")
                if not password:
                    continue
                manager.createRecord(site, username, password)
            elif choice == "2":
                siteList(manager)
                site = promptInput("Site Name")
                if not site:
                    continue
                record = manager.retrieveRecord(site)
                if record:
                    print(f"Username: {record['username']}\nPassword: {record['password']}")
                else:
                    print("No entry found.")
            elif choice == "3":
                site = promptInput("Site Name")
                if not site:
                    continue
                password = promptInput("Updated Password")
                if not password:
                    continue
                manager.updateRecord(site, password)
            elif choice == "4":
                
                siteList(manager)
                site = promptInput("Site Name")
                if not site:
                    continue
                manager.deleteRecord(site)
            elif choice == "5":
                siteList(manager)
            elif choice.lower() == "q":
                print("Farewell")
                break
            else:
                print("Invalid Choice")

if __name__ == "__main__":
    main()