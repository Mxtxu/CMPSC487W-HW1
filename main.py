from tkinter import *
from tkinter import ttk

def scan(*args):
    try:
        value = studentIdEntry.get()
        studentId.set(value)
    except ValueError:
        pass

def login():
    t = Toplevel(root)

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

studentId = StringVar()
ttk.Label(mainframe, textvariable=studentId).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Scan", command=scan).grid(column=3, row=1, sticky=W)

ttk.Button(mainframe, text="Admin Login", command=login).grid(column=3, row=2, sticky=W)

ttk.Label(mainframe, text="Student ID:").grid(column=1, row=1, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
root.bind("<Return>", scan)

root.mainloop()