#!/usr/bin/env python3

# The actual Hotel Reservation application. It requires setup before use.

# "If you're using global statements, you're doing something evil, hiding the fact that your code needs parameters, bloatful. It also won't work."

# TODOs

# NOTICE, TODO, WARNING, CODE, META: The usage of such variables for label and text was bad and needs to be changed in further releases. It is more overhead, harder-to-maintain and harder-to-debug. REPLACE ASAP.
# TODO: Import the person filler value from setup or manually define it for easier code
# TODO: Make this code have many versions. They should be better. Not limited to 18 rooms, customizable, free, beautiful etc. etc. etc.
# TODO: Add well-documented doctypes
# TODO: Make code slightly less fragile by implementing more advanced versions that allow CSV modifications of fields and rows (easy but not viable as of now since this version should be easy and specific)

# BUG: This program has a bug (more of a feature, no?) that nothing happens to the GUI nor the console after each bug. This is a "error-handling" feature.

import tkinter as tk # Imports tkinter
from tkinter import ttk # Imports tkk, new-generation widgets (UI)
from tkinter import messagebox # Imports message box capabilities (show errors, warnings, info messages)
from tkcalendar import Calendar # Imports a singular widget... a Tkinter widget for the calendar

from datetime import datetime # Imports datetime
import pandas as pd # Uses pandas to deal with the CSV database
import setup # Imports the setup file to set the program up
import tkinter.font as tkfont # For font customization

# Variables

fillerValue = setup.fillerValue # The value returned instead of NaN or False

baseCSVDatabase = setup.csvDatabasePath # By default, it's the database path but it can be changed!

windowBackgroundColor = "#F3F4F6" # Modern light background for better cross-platform look
buttonBackgroundColor = "#1976D2" # Accent blue for buttons
buttonForegroundColor = "#000000" # White button text
pureBlack = "#000000" # Deep gray-black for text

windowTitle = "Hotel Reservation App" # The window title which will always define the Tk window title
setRecordsWindowTitle = "Set Records" # Window title of the Toplevel set records Tk window

setRecordsButton = "Set Database Records" # The title of the button which allows editing of the CSV database
showAllRoomsButton = "Show All Rooms" # The title of the button that shows all rooms
showAllTakenRoomsButton = "Show All Taken Rooms" # The title of the button that shows all taken rooms
showAllNonTakenRoomsButton = "Show All Non Taken Rooms" # The title of the button that shows all non-taken rooms
searchRoomNumberLabel = "Search Room Number" # The label of the input that searches room numbers
searchRoomNumberColumn, searchRoomNumberColumn2, searchRoomNumberColumn3, searchRoomNumberColumn4 = "Room Number", "Taken", "Dates Taken", "People"

# SET RECORDS
chosenRoomNumberLabelText = "Room Number: " # The text of the label of the input that asks for the room number
isRoomNumberTakenLabelText = "Is Taken: " # The text of the label of the input that asks if the room number is taken or no
roomNumberTakenDatesLabelText = "Taken Dates: " # The text of the label of the input that asks the dates (start-end) of room taked
peopleLabelText = "People: " # The text of the label of the input that asks the total people in a taken room
submitButtonText = "Submit" # The text of the button of the Set Records window to submit the data

# Functions

def datetimeCheck(): # Checks and calculates the datetime of the third (takendates) field of the CSV file to do automatic and very precise datetime checking (every minute)
    global baseCSVDatabase, fillerValue, window         
    baseCSVDatabaseDF = pd.read_csv(baseCSVDatabase)
    for index, row in baseCSVDatabaseDF.iterrows():
        if row["taken"] == fillerValue or row["takendates"] == fillerValue or row["people"] == fillerValue:
            pass
        else:
            try:
                endingDateStr = row["takendates"].split("-")[1]
                endingDate = datetime.strptime(endingDateStr, "%m/%d/%Y")
                if datetime.today() > endingDate:
                    baseCSVDatabaseDF.at[index, "taken"] = fillerValue
                    baseCSVDatabaseDF.at[index, "takendates"] = fillerValue
                    baseCSVDatabaseDF.at[index, "people"] = 0
            except Exception as e:
                messagebox.showerror("Error", e)
    try:
        baseCSVDatabaseDF.to_csv(baseCSVDatabase, index=False)
    except PermissionError:
        messagebox.showerror("Bad Permissions", "You don't have the needed privileges to write to the file. Make sure you have administrator (sudo) mode!")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "This script has been modified or the files have been moved. Remove all program files and rerun the program for correct setup.")
    except OSError:
        messagebox.showerror("OS Error", "There's something wrong with your system's file system or file handling.")
    except ValueError: 
        messagebox.showerror("Data Error", "This script has been modified or tampered with which has resulted in bad value handling.")
    except Exception as e:
        messagebox.showerror("Error", e)
    window.after(60000, datetimeCheck) # Runs after the end of the function to always run itself every minute and when it runs itself every minute, it will execute this line of code to run itself every minute
    
def validateSearch(roomNumber): # Validates the room number search with many series of checks (REMOVE FUNCTION IF ROOM IS NOT WITHIN RANGE OF 101-106; 201-206; 301-306)
    if isinstance(roomNumber, str): # If room number is string...
       try:
           int(roomNumber) # Pyhack: If you need to only return True or False and want to check like these conditions, use int() to check if it's base 10 and return. If not base 10, it won't happen
           if int(roomNumber) >= 101 and int(roomNumber) <= 106:
               return True              
           elif int(roomNumber) >= 201 and int(roomNumber) <= 206:
               return True           
           elif int(roomNumber) >= 301 and int(roomNumber) <= 306:
               return True
           else:
               messagebox.showerror("Room Number Limitation", f"The room number doesn't fit the current room limit at the district. If the amount of rooms has improved since then, use a unrestricted version or contact the owner for further modifications.")         
               return False 
       except ValueError:
           messagebox.showerror("Bad Value", f"{roomNumber} is not a number")
           return False
       except Exception as e:
           messagebox.showerror("Error", e)
           return False 
           
def search(roomNumber): # Searches all rooms
    global baseCSVDatabase, fillerValue, searchRoomNumberTreeview
    baseCSVDatabaseDF = pd.read_csv(baseCSVDatabase)
    
    for row in searchRoomNumberTreeview.get_children():
        searchRoomNumberTreeview.delete(row)
    
    # This if statement should get removed if there are more rooms than specified
    if validateSearch(roomNumber) == True:  
        pass                        
    else:
        return None # This is my sneakiest workaround... return = stop, functions that just do results and don't return are stopped with return ;)
        
    for index, row in baseCSVDatabaseDF.iterrows():
        if int(row.iloc[0]) == int(roomNumber): # Once again, FutureWarning strikes and hates int(row[0])
            rows = list(row)
            rows[0] = int(rows[0])
            if rows[1] == fillerValue:
                searchRoomNumberTreeview.insert("", "end", values=rows, tags=("nontaken"))
                messagebox.showinfo("Success", "Room number search done successfully")
            else:
                searchRoomNumberTreeview.insert("", "end", values=rows, tags=("taken"))
                messagebox.showinfo("Success", "Room number search done successfully")
        else:
            pass
    
def submit(chosenRoom, isTaken, startTakenDate, endTakenDate, people): # Automatically submits the setRecords() data in a safe way and overwrites room data in database safely
    global baseCSVDatabase, fillerValue # Give me the database and the parameters... let's overwrite the data!
    baseCSVDatabaseDFCopy = pd.read_csv(baseCSVDatabase) # A copy (the) of the DF of CSV
    if chosenRoom == "": # These if statements make the specification of the room and the taken status essential
        messagebox.showerror("No Room Specified", "No room was chosen from the dropdown list!")
        return None 
    else:
        pass                      
    if isTaken == "":
        messagebox.showerror("Taken Status Not Specified", "The status of the room was not chosen from the dropdown list. The program can't tell if it is taken or not.")
        return None 
    else:
        pass
    if not isTaken == fillerValue: # If it is TAKEN... In other words, if it is NOT NOT taken... 
        try:
            int(people) # SNEAKY: Try to make people integer
        except ValueError: 
            messagebox.showerror("Not Valid People", "The number input must be base 10, amount of people can't be a non-number. It's also likely that's empty input.")
            return None 
        except Exception as e:
            messagebox.showerror("Error", e)
            return None 
        
        baseCSVDatabaseDFCopy.loc[baseCSVDatabaseDFCopy["room"] == int(chosenRoom)] = [int(chosenRoom), isTaken, f"{startTakenDate}-{endTakenDate}", int(people)] # Don't write unless...
        if not int(people) <= 0: # TODO: Quick workaround to check the validity of room taking (taken rooms won't have 0 or negative people). Function-alize it
            baseCSVDatabaseDFCopy.to_csv(baseCSVDatabase, index=False)
        else: # If the room HAS 0 people or less...
            messagebox.showerror("Logical Error", "Taken rooms cannot have 0 people or a negative amount of people. It doesn't make sense.") # Error and stop
    else: 
        baseCSVDatabaseDFCopy.loc[baseCSVDatabaseDFCopy["room"] == int(chosenRoom)] = [int(chosenRoom), fillerValue, fillerValue, 0]
        baseCSVDatabaseDFCopy.to_csv(baseCSVDatabase, index=False)
        messagebox.showinfo("Records Modified Successfully", f"Room Number: {chosenRoom}, {isTaken}")
        
def setRecords(): # Opens up a window which allows the editing of the CSV database 
    global setRecordsWindowTitle, windowBackgroundColor, buttonBackgroundColor, buttonForegroundColor, pureBlack, chosenRoomNumberLabelText, baseCSVDatabase, fillerValue, roomNumberTakenDatesLabelText, peopleLabelText, submitButtonText
    
    setRecordsWindow = tk.Toplevel()
    setRecordsWindow.title(setRecordsWindowTitle)
    setRecordsWindow.configure(background=windowBackgroundColor)

    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=11, family="Segoe UI")
    setRecordsWindow.option_add("*Font", default_font)

    sfrm = ttk.Frame(setRecordsWindow, padding=20)
    sfrm.pack(expand=True, fill=tk.BOTH)

    # Room Number
    ttk.Label(sfrm, text=chosenRoomNumberLabelText, foreground=pureBlack).pack(anchor="w", pady=(0, 4))
    chosenRoomNumberDropdown = ttk.Combobox(
        sfrm,
        state="readonly",
        values=[str(row.iloc[0]) for index, row in pd.read_csv(baseCSVDatabase).iterrows()],
        width=20
    )
    chosenRoomNumberDropdown.pack(fill=tk.X, pady=(0, 10))

    # Is Taken
    ttk.Label(sfrm, text=isRoomNumberTakenLabelText, foreground=pureBlack).pack(anchor="w", pady=(0, 4))
    isRoomNumberTakenDropdown = ttk.Combobox(
        sfrm,
        state="readonly",
        values=[fillerValue, "Taken"],
        width=20
    )
    isRoomNumberTakenDropdown.pack(fill=tk.X, pady=(0, 10))

    # Dates
    ttk.Label(sfrm, text=roomNumberTakenDatesLabelText, foreground=pureBlack).pack(anchor="w", pady=(0, 4))
    datesFrame = ttk.Frame(sfrm)
    datesFrame.pack(fill=tk.X, pady=(0, 10))
    roomNumberTakenDatesCalendarStart = Calendar(datesFrame, date_pattern="mm/dd/yyyy")
    roomNumberTakenDatesCalendarStart.pack(side=tk.LEFT, padx=(0, 8))
    roomNumberTakenDatesCalendarEnd = Calendar(datesFrame, date_pattern="mm/dd/yyyy")
    roomNumberTakenDatesCalendarEnd.pack(side=tk.LEFT)

    # People
    ttk.Label(sfrm, text=peopleLabelText, foreground=pureBlack).pack(anchor="w", pady=(0, 4))
    peopleEntry = ttk.Entry(sfrm)
    peopleEntry.pack(fill=tk.X, pady=(0, 16))

    def close_and_submit():
        submit(
            chosenRoomNumberDropdown.get(),
            isRoomNumberTakenDropdown.get(),
            roomNumberTakenDatesCalendarStart.get_date(),
            roomNumberTakenDatesCalendarEnd.get_date(),
            peopleEntry.get()
        )
        setRecordsWindow.destroy()

    ttk.Button(
        sfrm,
        text=submitButtonText,
        style="Accent.TButton",
        command=close_and_submit
    ).pack(pady=(4, 0), ipadx=10, ipady=4)

def showAllRooms():
    global baseCSVDatabase, searchRoomNumberTreeview, fillerValue
    baseCSVDatabaseDF = pd.read_csv(baseCSVDatabase)
    for row in searchRoomNumberTreeview.get_children():
        searchRoomNumberTreeview.delete(row)
    for index, row in baseCSVDatabaseDF.iterrows():
        rows = list(row)
        rows[0] = int(rows[0])
        if rows[1] == fillerValue:
            searchRoomNumberTreeview.insert("", "end", values=rows, tags=("nontaken"))
        else:
            searchRoomNumberTreeview.insert("", "end", values=rows, tags=("taken"))
    messagebox.showinfo("Success", "All rooms shown")

def showAllTakenRooms():
    global baseCSVDatabase, searchRoomNumberTreeview, fillerValue
    baseCSVDatabaseDF = pd.read_csv(baseCSVDatabase)
    for row in searchRoomNumberTreeview.get_children():
        searchRoomNumberTreeview.delete(row)
    for index, row in baseCSVDatabaseDF.iterrows():
        row = list(row)
        row[0] = int(row[0])
        if row[1] == fillerValue:
            pass
        else:
            searchRoomNumberTreeview.insert("", "end", values=row, tags=("taken",))
    messagebox.showinfo("Success", "All taken rooms shown")
    
def showAllNonTakenRooms():
    global baseCSVDatabase, searchRoomNumberTreeview, fillerValue
    baseCSVDatabaseDF = pd.read_csv(baseCSVDatabase)
    for row in searchRoomNumberTreeview.get_children():
        searchRoomNumberTreeview.delete(row)
    for index, row in baseCSVDatabaseDF.iterrows():
        row = list(row)
        row[0] = int(row[0])
        if row[1] == fillerValue:
            searchRoomNumberTreeview.insert("", "end", values=row, tags=("nontaken",))
        else:
            pass
    messagebox.showinfo("Success", "All non-taken rooms shown")
    
def main():
    global window, windowBackgroundColor, buttonBackgroundColor, buttonForegroundColor, pureBlack, windowTitle, showAllRoomsButton, showAllTakenRoomsButton, showAllNonTakenRoomsButton, searchRoomNumberLabel, searchRoomNumberColumn, searchRoomNumberColumn2, searchRoomNumberColumn3, searchRoomNumberColumn4, setRecords, searchRoomNumberTreeview, style

    window = tk.Tk()
    window.title(windowTitle)
    window.attributes("-fullscreen", True)
    window.configure(bg=windowBackgroundColor)
    
    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))
    window.bind("<F11>", lambda event: window.attributes("-fullscreen", True))
    
    # Set modern ttk theme
    style = ttk.Style(window)
    if "vista" in style.theme_names():
        style.theme_use("vista")
    else:
        style.theme_use("clam")

    # Set global font
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=11, family="Segoe UI")
    window.option_add("*Font", default_font)

    # Enhanced ttk button style
    style.configure("Accent.TButton",
        foreground=buttonForegroundColor, background=buttonBackgroundColor, font=('Segoe UI', 11, 'bold'),
        borderwidth=0, focusthickness=1, focuscolor=buttonBackgroundColor)

    style.map("Accent.TButton",
        background=[('active', '#1565C0'), ('pressed', '#1565C0')],
        foreground=[('disabled', '#ccc')])

    frm = ttk.Frame(window, padding=32)
    frm.pack(expand=True, fill=tk.BOTH)

    btnrow = ttk.Frame(frm)
    btnrow.pack(fill=tk.X, pady=(0, 12))
    ttk.Button(btnrow, text=setRecordsButton, style="Accent.TButton", command=setRecords).pack(side=tk.LEFT, padx=4)
    ttk.Button(btnrow, text=showAllRoomsButton, style="Accent.TButton", command=showAllRooms).pack(side=tk.LEFT, padx=4)
    ttk.Button(btnrow, text=showAllTakenRoomsButton, style="Accent.TButton", command=showAllTakenRooms).pack(side=tk.LEFT, padx=4)
    ttk.Button(btnrow, text=showAllNonTakenRoomsButton, style="Accent.TButton", command=showAllNonTakenRooms).pack(side=tk.LEFT, padx=4)

    ttk.Label(frm, text=searchRoomNumberLabel, font=("Segoe UI", 14, "bold"), foreground=pureBlack).pack(pady=(0, 8))
    searchFrame = ttk.Frame(frm)
    searchFrame.pack(fill=tk.X, pady=(0, 12))
    searchRoomNumberInput = ttk.Entry(searchFrame, width=16)
    searchRoomNumberInput.pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(searchFrame, text="Search", style="Accent.TButton",
        command=lambda: search(searchRoomNumberInput.get())).pack(side=tk.LEFT)

    treeFrame = ttk.Frame(frm)
    treeFrame.pack(expand=True, fill=tk.BOTH)
    searchRoomNumberTreeview = ttk.Treeview(
        treeFrame,
        columns=(searchRoomNumberColumn, searchRoomNumberColumn2, searchRoomNumberColumn3, searchRoomNumberColumn4),
        show="headings",
        height=20
    )
    searchRoomNumberTreeview.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    for col in (searchRoomNumberColumn, searchRoomNumberColumn2, searchRoomNumberColumn3, searchRoomNumberColumn4):
        searchRoomNumberTreeview.heading(col, text=col)
        searchRoomNumberTreeview.column(col, anchor=tk.CENTER, width=120)

    style.map("Treeview", background=[("selected", "#1976D2")])
    searchRoomNumberTreeview.tag_configure("taken", background="#FFCDD2")
    searchRoomNumberTreeview.tag_configure("nontaken", background="#C8E6C9")

    treeScroll = ttk.Scrollbar(treeFrame, orient="vertical", command=searchRoomNumberTreeview.yview)
    searchRoomNumberTreeview.configure(yscroll=treeScroll.set)
    treeScroll.pack(side=tk.RIGHT, fill=tk.Y)

    window.bind("<F11>", lambda event: window.attributes("-fullscreen", True))
    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

    datetimeCheck() # Calls datetimeCheck() every program run which calls itself every minute (60 seconds) with window.after() which schedules tasks

    window.mainloop()
    
if __name__ == "__main__":
    setup.setup()
    main()
else:
    pass
