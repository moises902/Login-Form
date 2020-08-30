import tkinter as tk
from tkinter import font as tkfont
import mysql.connector
import hashlib

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="Lightvine21!",
    database='PASSWORD_DATABASE',
    auth_plugin='mysql_native_password')
cursor = db.cursor()

# SampleApp class was copied from Bryan Oakley's code
# Link: https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=14, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def quit(self):
        self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Please Enter your information:", font=controller.title_font)
        label.grid(row = 0, columnspan = 2)

        prompt_user = tk.Label(self, text = "Username: ")
        prompt_passwd = tk.Label(self, text = "Password: ")
        prompt_user.grid(row = 1, column = 0)
        prompt_passwd.grid(row = 2, column = 0)

        user_entry = tk.Entry(self)
        pass_entry = tk.Entry(self, show = '*')
        user_entry.grid(row = 1, column = 1)
        pass_entry.grid(row = 2, column = 1)

        button1 = tk.Button(self, text="Sumbit", command=lambda: check(self, parent, controller, str(user_entry.get()), str(pass_entry.get())))
        button1.grid(row = 3, column = 1)

# This method is responsible for authenticating the user by comparing hash values
def check(self, parent, controller, user_entry, pass_entry):
    
    cursor.execute("SELECT USER_ID FROM USER_PASS")
    list_names = cursor.fetchall()
    name_found = False
    
    for x in list_names: 
        # Checks if the username entry is in the database
        name = str(x[0])
        if name == user_entry: 
            name_found = True   

    if name_found:    
        cursor.execute("SELECT SALT FROM USER_PASS WHERE USER_ID = \'{}\'".format(user_entry))
        salt = str(cursor.fetchone()[0])
        cursor.execute("SELECT HASH_CODE FROM USER_PASS WHERE USER_ID = \'{}\'".format(user_entry))
        hashcode = str(cursor.fetchone()[0])

        input_hash = hashlib.md5(bytes(salt, 'ascii') + bytes(pass_entry, 'ascii')).hexdigest()

        # Checks if the user input hash matches the hash stored in the database
        if input_hash == hashcode:
            controller.show_frame('PageOne')
        else:
            controller.show_frame('PageTwo')
    else:
        controller.show_frame('PageTwo') 
    
# Frame when a correct user is logged in
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is a secure page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Logout", command=lambda: self.quit())
        button.pack()

#This frame is when a user enters in the wrong credentials
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Please Enter your information:", font=controller.title_font)
        label.grid(row = 0, columnspan = 2)

        prompt_user = tk.Label(self, text = "Username: ")
        prompt_passwd = tk.Label(self, text = "Password: ")
        prompt_user.grid(row = 1, column = 0)
        prompt_passwd.grid(row = 2, column = 0)

        err = tk.Label(self, text = "Incorrect username/password", foreground = "red")
        err.grid(row = 3, column = 1)

        user_entry = tk.Entry(self)
        pass_entry = tk.Entry(self, show = '*')
        user_entry.grid(row = 1, column = 1)
        pass_entry.grid(row = 2, column = 1)

        button1 = tk.Button(self, text="Sumbit", command=lambda: [check(self, parent, controller, str(user_entry.get()), str(pass_entry.get())), 
                                                                    pass_entry.delete(0, 'end'), user_entry.delete(0, 'end') ])
        button1.grid(row = 4, column = 1)

# Ends the gui and closes connection with the database
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

db.close()