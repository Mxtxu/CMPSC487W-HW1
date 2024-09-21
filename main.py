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

    # Placeholder for isActive field.
    isActive = True
    data = {
        'studentId': value,
        'timestamp': epoch_timestamp,
        'type': userType,
        'status': isActive
    }
    scanDB.add(data)

#For now, login is just '2' for the password.
# TO-DO, implement 'credentials' for admins.

adminFrame = None
def login():
    def renderLeft(data):
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


            for row, record in enumerate(data, start=1):
                doc = record.to_dict()
                timestamp = doc.get('timestamp', 'N/A')
                readable_date = str(datetime.datetime.fromtimestamp(timestamp))
                ttk.Label(finalFrame, text=doc.get('studentId', 'N/A')).grid(row = row, column = 0, sticky="n", padx=10, pady=5)
                ttk.Label(finalFrame, text=readable_date).grid(row= row, column=1, sticky="n", padx=10, pady=5)
                ttk.Label(finalFrame, text=doc.get('type', 'N/A')).grid(row= row, column=2, sticky="n", padx=10, pady=5)

    def filterSingleDate(*args):
        year = startyearValue.get()
        month =  startmonthValue.get()
        day = startdayValue.get()


        epoch = datetime.datetime(year, month, day).timestamp()
        data = scanDB.where(field_path='timestamp', op_string='==', value=epoch)
        renderLeft(data.stream())


    def filterTimeRange():
        year1 = startyearValue.get()
        month1 = startmonthValue.get()
        day1 = startdayValue.get()

        year2 = endyearValue.get()
        month2 = endmonthValue.get()
        day2 = enddayValue.get()

        epoch1 = datetime.datetime(year1, month1, day1).timestamp()
        epoch2 = datetime.datetime(year2, month2, day2).timestamp()
        data = scanDB.where(field_path='timestamp', op_string='>=', value=epoch1).where(field_path='timestamp', op_string='<=', value=epoch2)
        renderLeft(data.stream())

    def filterStudentId():
        studId = newId.get()

        print(studId)
        data = scanDB.where(field_path='studentId', op_string='==', value=studId)

        renderLeft(data.stream())

    def resetFrame():
        defaultRecords = scanDB.stream()
        renderLeft(defaultRecords)

    records = scanDB.stream()

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
