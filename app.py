import  tkinter  as tk
from tkinter import simpledialog, messagebox, ttk
from VaultManager import VaultManager
import json
import os

class vaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Vault")
        self.geometry("700x400")
        self.manager = VaultManager()
        self.dataLoaded = False
        self.buildLogin()
    
    def buildLogin(self):
        self.clear()
        tk.Label(self, text="Enter Master Password").pack(pady=10)
        self.masterPwEntry = tk.Entry(self, show="*")
        self.masterPwEntry.pack()

        tk.Button(self, text="Unlock Vault", command = self.unlock).pack(pady=10)
    
    def unlock(self):
        password = self.masterPwEntry.get()
        if not password:
            messagebox.showerror("Error", "Password Required")
            return
        if self.manager.loadVault(password):
            self.buildMainMenu()
        else:
            messagebox.showerror("Error", "Wrong Password or corrupted Vault")
    
    def buildMainMenu(self):
        self.clear()
        tk.Label(self, text = "Vault Records").pack(pady = 5)

        frame = ttk.Frame(self)
        frame.pack(expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.siteList = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        for site in self.manager.listSites():
            self.siteList.insert(tk.END, site)
        self.siteList.pack(side=tk.LEFT, fill = tk.BOTH, expand=True)
        scrollbar.config(command=self.siteList.yview)

        buttonFrame = ttk.Frame(self)
        buttonFrame.pack(pady = 10)
        tk.Button(buttonFrame, text="Add Record", command=self.addRecord).pack(side=tk.LEFT, padx= 5)
        tk.Button(buttonFrame, text="View Record", command=self.viewRecord).pack(side=tk.LEFT,  padx = 5 )
        tk.Button(buttonFrame, text="Update Record", command=self.updRecord).pack(side=tk.LEFT,  padx = 5 )
        tk.Button(buttonFrame, text="Delete Record", command=self.delRecord).pack(side=tk.LEFT, padx = 5 )
        tk.Button(self, text="Exit", command=self.quit).pack(side=tk.BOTTOM, pady=5)
        
    def viewRecord(self):
        selection =  self.siteList.curselection()
        if not selection:
            messagebox.showwarning("Select site", "No site selected")
            return
        
        site = self.siteList.get(selection[0])
        record = self.manager.retrieveRecord(site)
        messagebox.showinfo(f"{site}", f"Username: {record['username']}\nPassword: {record['password']}")

    def addRecord(self):
        site = simpledialog.askstring("Site", "Enter site name")
        if not site:
            return
        if self.manager.recordExists(site):
            messagebox.showwarning("Duplicate", "That site already exists.")
            return

        username = simpledialog.askstring(
            "Username",
            "Enter username"
        )
        if not username:
            return
        password = simpledialog.askstring(
            "Password", 
            "Enter password"
        )
        if not password:
            return
        
        self.manager.createRecord(site, username, password)
        self.buildMainMenu()

    def delRecord(self):
        selection =  self.siteList.curselection()
        if not selection:
            messagebox.showwarning("Select site", "No site selected")
            return
        
        site = self.siteList.get(selection[0])
        self.manager.deleteRecord(site)
        messagebox.showinfo("SDeletion", f"Record for {site} has been deleted.")
        self.buildMainMenu()
    
    def updRecord(self):
        selection =  self.siteList.curselection()
        if not selection:
            messagebox.showwarning("Select site", "No site selected")
            return
        
        site = self.siteList.get(selection[0])
        password = simpledialog.askstring("Password", "Enter new password")
        self.manager.updateRecord(site, password)
        messagebox.showinfo("Updated", f"Record for {site} has been updated.")

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = vaultApp()
    app.mainloop()