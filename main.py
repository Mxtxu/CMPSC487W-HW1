import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Firebase setup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./firestoreinfo/dbKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
scanDB = db.collection('scanHistory')


def scan(*args):

    value = int(studentIdEntry.get())

    today = datetime.date.today()


    start_of_day = datetime.datetime.combine(today, datetime.time.min)


    epoch_timestamp = int(start_of_day.timestamp())

    # Format to get just the year, month, and day


    userType = 'student'
    data = {
        'studentId': value,
        'timestamp': epoch_timestamp,
        'type': userType
    }
    scanDB.add(data)

#For now, login is just '2' for the password.
# TO-DO, implement 'credentials' for admins.




needFilter = False

adminFrame = None
def login():
    username = usernameEntry.get()
    password = passwordEntry.get()
    if password == "2":
        window = Toplevel()
        window.title("Scan History")

        # Now we'll make the part of the window that allows for all the filtering.
        filterFrame = tk.Frame(window, bg="lightgray", width=200)
        filterFrame.pack(side="right", fill="y")
        tk.Label(filterFrame, text="Filtering:", bg="lightgray").grid(column=1, row=0, pady=5)

        tk.Label(filterFrame, text="Start Date :", bg="lightgray").grid(column=1, row=1)
        tk.Label(filterFrame, text="Fill this to filter by single date", bg="lightgray").grid(column=1, row=2)
        # Year Month Day Columns
        tk.Label(filterFrame, text="Year", bg="lightgray").grid(column=1, row=3)
        tk.Label(filterFrame, text="Month", bg="lightgray").grid(column=2, row=3)
        tk.Label(filterFrame, text="Day", bg="lightgray").grid(column=3, row=3)


        startyearValue= IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=startyearValue).grid(column=1, row=4)

        startmonthValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=startmonthValue).grid(column=2, row=4)

        startdayValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=startdayValue).grid(column=3, row=4)

        tk.Label(filterFrame, text="End Date :", bg="lightgray").grid(column=1, row=5)

        endyearValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=endyearValue).grid(column=1, row=6)

        endmonthValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=endmonthValue).grid(column=2, row=6)

        enddayValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=enddayValue).grid(column=3, row=6)

        ttk.Button(filterFrame, text="Filter by Single Date", command=filterSingleDate).grid(column=1, row=7, sticky=W)
        ttk.Button(filterFrame, text="Filter by Time Range", command=filterTimeRange).grid(column=2, row=7, sticky=W)

        newId = IntVar()
        tk.Label(filterFrame, text="Filter by Student Id:", bg="lightgray").grid(column=1, row=8, sticky=W)
        ttk.Entry(filterFrame, width=10, textvariable=newId).grid(column=2, row=8, sticky=W)
        ttk.Button(filterFrame, text="Filter by Student Id", command=filterStudentId).grid(column=3, row=8, sticky=W)

        ttk.Button(filterFrame, text="Reset Filters", command=resetFrame).grid(column=1, row=9, sticky=W)
        renderLeft(records)


        window.mainloop()


root = Tk()
root.title("SunLab Scanner")

mainframe = ttk.Frame(root, padding="350 350 350 350", borderwidth=4, relief='sunken')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Entry box
studentIdEntry = StringVar()
id_entry = ttk.Entry(mainframe, width=7, textvariable=studentIdEntry)
id_entry.grid(column=2, row=1, sticky=(W, E))

# Password entry for Admin
passwordEntry = StringVar()
password_entry = ttk.Entry(mainframe, width = 10, textvariable=passwordEntry)
password_entry.grid(column=2, row=2)

studentId = StringVar()


ttk.Button(mainframe, text="Scan", command=scan).grid(column=3, row=1, sticky=W)

ttk.Button(mainframe, text="Admin Login", command=login).grid(column=3, row=2, sticky=W)

ttk.Label(mainframe, text="Student ID:").grid(column=1, row=1, sticky=W)

ttk.Label(mainframe, text="Password: ").grid(column=1, row=2, sticky=W)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
root.bind("<Return>", scan)

root.mainloop()

# Testing commit on Mac
