import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Firebase setup
import firebase_admin
from firebase_admin import credentials, firestore

# Setting up Firebase credentials and db access.
cred = credentials.Certificate("./firestoreinfo/dbKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Global variables we'll use later
# ScanDB is the scanHistory collection
scanDB = db.collection('scanHistory')

# adminFrame is used to track and make sure we don't create duplicate
# adminFrames in the admin window.
adminFrame = None

# This is where the user can 'scan' their id. It takes an integer input.
# And then stores the id, time, and type of user into the database.
def scan(*args):
    value = int(studentIdEntry.get())
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    epoch_timestamp = int(start_of_day.timestamp())
    userType = 'student'

    # Placeholder value for isActive status.
    isActive = True

    data = {
        'studentId': value,
        'timestamp': epoch_timestamp,
        'type': userType,
        'isActive': isActive
    }
    scanDB.add(data)

#For now, login is just '2' for the password.
# TO-DO, implement 'credentials' for admins.

# Kind of unwieldy in retrospect but logging in actually renders the whole admin screen.
def login():
    # This function will actually render the table. We make sure to destroy
    # the frame if there is an existing frame.
    def renderTable(data):
        global adminFrame
        if adminFrame is not None:
            adminFrame.destroy()
            adminFrame = None

        if adminFrame is None:
            adminFrame = ttk.Frame(window, borderwidth=4, relief='sunken')
            adminFrame.pack(side='left', fill='both', expand=True)
            canvas = tk.Canvas(adminFrame, width=500, height=800)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(adminFrame, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            finalFrame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=finalFrame, anchor="nw")

            ttk.Label(finalFrame, text="Student ID:").grid(column=0, row=0, sticky=N, padx=50, pady=50)
            ttk.Label(finalFrame, text="Time: ").grid(column=1, row=0, sticky=N, padx=50, pady=50)
            ttk.Label(finalFrame, text="Type: ").grid(column=2, row=0, sticky=N, padx=50, pady=50)


            # This renders the actual records
            for row, record in enumerate(data, start=1):
                doc = record.to_dict()
                timestamp = doc.get('timestamp', 'N/A')
                readable_date = str(datetime.datetime.fromtimestamp(timestamp))
                ttk.Label(finalFrame, text=doc.get('studentId', 'N/A')).grid(row = row, column = 0, sticky="n", padx=10, pady=5)
                ttk.Label(finalFrame, text=readable_date).grid(row= row, column=1, sticky="n", padx=10, pady=5)
                ttk.Label(finalFrame, text=doc.get('type', 'N/A')).grid(row= row, column=2, sticky="n", padx=10, pady=5)



    # Used when we want to filter by a single date.
    # Queries the DB and returns the data from that specific date.
    def filterSingleDate(*args):
        year = startYearValue.get()
        month =  startMonthValue.get()
        day = startDayValue.get()


        epoch = datetime.datetime(year, month, day).timestamp()
        data = scanDB.where(field_path='timestamp', op_string='==', value=epoch)
        renderTable(data.stream())

    # Same as filterSingleData but does this for a time range instead.
    def filterTimeRange():
        year1 = startYearValue.get()
        month1 = startMonthValue.get()
        day1 = startDayValue.get()

        year2 = endYearValue.get()
        month2 = endMonthValue.get()
        day2 = endDayValue.get()

        epoch1 = datetime.datetime(year1, month1, day1).timestamp()
        epoch2 = datetime.datetime(year2, month2, day2).timestamp()
        data = scanDB.where(field_path='timestamp', op_string='>=', value=epoch1).where(field_path='timestamp', op_string='<=', value=epoch2)
        renderTable(data.stream())

    # Same as the previous functions but filters based on studentId
    def filterStudentId():
        studId = newId.get()

        print(studId)
        data = scanDB.where(field_path='studentId', op_string='==', value=studId)

        renderTable(data.stream())

    # Function that's used in the reset button in case we want to reset
    # the table.
    def resetTable():
        defaultRecords = scanDB.stream()
        renderTable(defaultRecords)

    records = scanDB.stream()

    password = passwordEntry.get()
    if password == "2":
        window = Toplevel()
        window.title("Scan History")

        # Now we'll make the part of the window that allows for all the filtering.
        # Creates the labels and input boxes for filtering.

        filterFrame = tk.Frame(window, bg="lightgray", width=200)
        filterFrame.pack(side="right", fill="y")
        tk.Label(filterFrame, text="Filtering:", bg="lightgray", font=("Helvetica", 24, "bold")).grid(column=1, row=0, pady=5)

        tk.Label(filterFrame, text="Start Date :", bg="lightgray").grid(column=1, row=1)
        tk.Label(filterFrame, text="Fill this to filter by single date", bg="lightgray").grid(column=1, row=2)

        # Year Month Day Columns
        tk.Label(filterFrame, text="Year", bg="lightgray").grid(column=1, row=3)
        tk.Label(filterFrame, text="Month", bg="lightgray").grid(column=2, row=3)
        tk.Label(filterFrame, text="Day", bg="lightgray").grid(column=3, row=3)

        startYearValue= IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=startYearValue).grid(column=1, row=4)

        startMonthValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=startMonthValue).grid(column=2, row=4)

        startDayValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=startDayValue).grid(column=3, row=4)

        tk.Label(filterFrame, text="End Date :", bg="lightgray").grid(column=1, row=5)

        endYearValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=endYearValue).grid(column=1, row=6)

        endMonthValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=endMonthValue).grid(column=2, row=6)

        endDayValue = IntVar()
        ttk.Entry(filterFrame, width=10, textvariable=endDayValue).grid(column=3, row=6)

        ttk.Button(filterFrame, text="Filter by Single Date", command=filterSingleDate).grid(column=1, row=7, sticky=W, padx=10, pady=10)
        ttk.Button(filterFrame, text="Filter by Time Range", command=filterTimeRange).grid(column=2, row=7, sticky=W, padx=10, pady=10)

        newId = IntVar()
        tk.Label(filterFrame, text="Filter by Student Id:", bg="lightgray").grid(column=1, row=8, sticky=W)
        ttk.Entry(filterFrame, width=10, textvariable=newId).grid(column=2, row=8, sticky=W)
        ttk.Button(filterFrame, text="Filter by Student Id", command=filterStudentId).grid(column=3, row=8, sticky=W, padx=10, pady=10)

        ttk.Button(filterFrame, text="Reset Filters", command=resetTable).grid(column=1, row=9, sticky=W, padx=10, pady=10)
        renderTable(records)

        window.mainloop()

# Makes the main login/scan screen.
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

# Buttons for scanning an ID and button for the Admin Login
ttk.Button(mainframe, text="Scan", command=scan).grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="Admin Login", command=login).grid(column=3, row=2, sticky=W)

# Labels for the input boxes.
ttk.Label(mainframe, text="Student ID:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Password: ").grid(column=1, row=2, sticky=W)

root.bind("<Return>", scan)

root.mainloop()


