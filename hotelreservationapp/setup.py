#!/usr/bin/env python3

# Setup file for Hotel Reservation App. Required to be ran at least once to ensure program files setup

# Libraries

from os import mkdir, path # Imports simple functions from the os module to make a directory and to check file memory usage
from pathlib import Path # Imports pathlib to have a POSIX-compliant standards-compliant all-platforms path for the directory and database creation
import pandas as pd # Imports pandas which is used to setup the CSV file

# Function to set up the base CSV database with a functional base that includes all rooms and None values for all non-defined values

# FILLER VALUES; CHANGES TO MAIN APP ARE INSTANT. ONLY CHANGE FOR LOCALIZATION PURPOSES. A FILLER VALUE IS A VALUE WHICH OTHERWISE IS FALSE. IT IS THERE TO SIMPLY FILL THE DATA (IT'S NOT ACTUALLY TRUE). 

fillerValue = str("Not taken") # Filler value instead of None (which returns NaN) or False (boolean value which returns False) for user. This is used for the taken, taken dates values.
numberFillerValue = int(0) # Filler value for the number of people. Better than the real filler value and more awesome. This just fills up the dataset with the user-friendlier value. USed for people amount.
 
def setupBaseCSVDatabase(): # Fully set up the baseCSVDatabase and polish it for use
    global fillerValue
    rooms = []
    noneValues = 0
    for room in range(101, (106 + 1)): 
        rooms.append(int(room))
        noneValues += 1
    for room in range(201, (206 + 1)):
        rooms.append(int(room))
        noneValues += 1
    for room in range(301, (306 + 1)):
        rooms.append(int(room))
        noneValues += 1
    return rooms, [fillerValue] * noneValues, [numberFillerValue] * noneValues # Returns a tuple with one list of the total rooms and a list of None (NaN) filler values for the rooms

# Variables

programFilesPath = Path.home() / "HotelReservationApp"
csvDatabasePath = programFilesPath / "database.csv"
baseCSVDatabase = pd.DataFrame({ # This is a useful dataframe (base database) to hold actual data. It just makes CSV fields and puts the rooms
    "room": setupBaseCSVDatabase()[0],
    "taken": setupBaseCSVDatabase()[1],
    "takendates": setupBaseCSVDatabase()[1],
    "people": setupBaseCSVDatabase()[2]
})

# Functions

def createCSVBase(): # Creates the base format of the CSV database itself
    global baseCSVDatabase, csvDatabasePath
    try:
        baseCSVDatabase.to_csv(csvDatabasePath, index=False)
    except FileNotFoundError:
        raise FileNotFoundError("The file wasn't found.")
    except PermissionError:
        raise PermissionError("You don't have the needed privileges to create the file. Make sure you have administrator (sudo) mode!")
    except ValueError:
        raise ValueError("The DataFrame is in a bad state; it doesn't have enough values for all fields or it is invalid.")
    except Exception as e:
        print(e)
    
    
def createCSV(): # Creates the CSV database itself
    global csvDatabasePath
    try:
        with open(csvDatabasePath, "x") as file:
            file.close()
    except FileExistsError:
        raise FileExistsError("The CSV database already exists.")  
    except PermissionError:
        raise PermissionError("You don't have the needed privileges to create the file. Make sure you have administrator (sudo) mode!")    
    except OSError:
        raise OSError("Your operating system is corrupted, file system is in a bad state or something else is wrong.")
    except Exception as e:
        print(e)        

def createProgramFilesPath():
    global programFilesPath
    try:
        mkdir(programFilesPath)
    except PermissionError:
        raise PermissionError("You don't have the needed privileges to create the file. Make sure you have administrator (sudo) mode!")
    except NotADirectoryError:
        raise NotADirectoryError("A directory isn't being made. Are you making a file or a corrupted location?")
    except OSError:
        raise OSError("Your operating system is corrupted, file system is in a bad state or something else is wrong.")
    except Exception as e:
        print(e)
        
def setup(): # Handles the setup
    global programFilesPath, csvDatabasePath
    if programFilesPath.exists():
        if csvDatabasePath.exists():
            if path.getsize(csvDatabasePath) == 0: # If the file is 0 bytes, create it
                createCSVBase()
            else:
                pass                         
        else: # If the file doesn't exist, create it and it's layout
            createCSV() 
            createCSVBase()        
    else: # If the directory doesn't exist, the CSV database will not exist and it certainly won't have content over it...
        createProgramFilesPath()
        createCSV() 
        createCSVBase()
        
if __name__ == "__main__":
    setup()
else: # If the module is being ran by an app or something else, it should run the functions and everything itself
    pass
