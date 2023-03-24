import tkinter as tk
from tkinter import *
import os
import sys
from tkinter import filedialog
import ntplib
from time import ctime
# sys.path.insert(0, 'UI_Han/BalanceProblem')
import ButtonGrid
import SignInWindow
import TransferScreen
import ButtonGrid
import UnloadContainersScreen
import modifyGrid
import pathlib

# USER = "DEFAULT"
global MainMenuUser
def appendLoadContainer(name):
    print('\n')
    name=name_var.get()
    
    loadInput.append(name)
    for i in loadInput:
        print(i)

def assignPastUser():
    SignInWindow.pastUser = SignInWindow.username
    
    # MainMenuUser = SignInWindow.username


def addSignInLogEvent():
    f = open("KeoghLongBeach2023.txt", "a")
    print("start addSignInLogEvent()") 
    # addLogEvent(("UserSwitch", getDateTime(), f"{SignInWindow.pastUser} signs out", f"{USER} signs in"))
    line = getDateTime() + f"{SignInWindow.username} signs in\n"
    f.write(line)
    print(line)

def getDateTime():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    currDateTime = ctime(response.tx_time)
    month = currDateTime[4:10]
    clock = currDateTime[11:16] 
    year = currDateTime[20:]

    # print(currDateTime)
    logDateTime = month + " " + year + ": " + clock + " "
    # print(logDateTime)
    return logDateTime

# MAIN MENU WINDOW (FIRST MENU)
def mainMenu():
    global menuRoot
    menuRoot = tk.Tk()
    menuRoot.geometry("700x400")
    # menuRoot.eval('tk::PlaceWindow . top')
    menuRoot.title("Main Menu")
    menuRoot.configure(background="white")
    global name_var
    name_var=tk.StringVar()

    # TITLE
    mainMenuTitleLabel = Label(menuRoot, text= "MAIN MENU", bg='white', fg="black", font=("Cambria", 20, "bold"))

    # SIGN IN BUTTON
    signInButton = tk.Button(menuRoot,text="Sign In",width=25,height=2, bg="#5465ff", fg="black", command=lambda: [SignInWindow.startUp(), assignPastUser(), addSignInLogEvent()])

    # IMPORT MANIFEST BUTTON
    importFileButton = tk.Button(text="Import Manifest",command=importFile, width=25, height=2, bg="#788bff", fg="black")
    
    # TRANSFER BUTTON
    transferButton = Button(menuRoot,text="Transfer",width=25,height=2,bg="#9bb1ff",fg="black",  command = transferWin) # opens the window for Transfer

    # BALANCE BUTTON
    balanceButton = tk.Button(menuRoot, text="Balance", width=25, height=2, bg="#bfd7ff", fg="black", command=lambda: ButtonGrid.main(SignInWindow.username)) #runBalance()

    # FIND OUTBOUND MANIFEST BUTTON
    buttonFile = tk.Button(text="Find Outbound Manifest", command=openFile, width=25, height=2, bg="#e2fdff", fg='black')
    
    
    

    mainMenuTitleLabel.pack(pady=10) 
    signInButton.pack(pady=5)
    importFileButton.pack(pady=5) 
    transferButton.pack(pady=5)
    balanceButton.pack(pady=5)
    buttonFile.pack(pady=5)
 
    menuRoot.mainloop() 

def openFile(): #https://www.youtube.com/watch?v=q8WDvrjPt0M
    filep = filedialog.askopenfilename(title= "Manifest File", filetypes= (("text files",".txt"), ("all files", ".*")))
    file = open(filep,'r')
    print(file.read())
    file.close()

def importFile(): 
    global manifest_filepath
    manifest_filepath = filedialog.askopenfilename()
    print(manifest_filepath)

    f = open("KeoghLongBeach2023.txt", "a")
    print("start addImportFileLogEvent()") 
    # addLogEvent(("UserSwitch", getDateTime(), f"{SignInWindow.pastUser} signs out", f"{USER} signs in"))

    path = pathlib.PurePath(manifest_filepath)
    txtFile = path.name
    file = txtFile.split(".txt")
    shipName = file[0]

    line = getDateTime() + f"Manifest {shipName}.txt is opened\n"
    f.write(line)
    print(line)

    TransferScreen.assignManifest(manifest_filepath)
    UnloadContainersScreen.assignManifest(manifest_filepath)
    modifyGrid.assignManifest(manifest_filepath)
    ButtonGrid.assignManifest(manifest_filepath)
    return manifest_filepath

# TRANSFER PROBLEM WINDOW
def transferWin():
    global loadInput
    loadInput = []
    TRANSFER = True
    print("After TRANSFER is selected it is", TRANSFER)
    transferWindow = tk.Toplevel()
    transferWindow.title("TRANSFER")
    transferWindow.geometry("300x200")
    transferWindow.configure(background="white")

    # TRANSFER TITLE
    transferLabel = tk.Label(transferWindow, text = "TRANSFER", bg='white', fg="black", font=("Cambria", 14, "bold"))
    
    # LOAD BUTTON
    loadBut = tk.Button(transferWindow,text="Load",width=25,height=2,bg="#5465ff",fg="black",command = loadWin)

    # UNLOAD BUTTON
    unloadBut = tk.Button(transferWindow,text="Unload",width=25,height=2,bg="#788bff",fg="black", command=lambda: UnloadContainersScreen.main())

    # BEGIN ORDERING BUTTON
    beginOrderBut = tk.Button(transferWindow,text="Begin Ordering", width=25,height=2, bg="#9bb1ff",fg="black", command=lambda: [printAllContainers(), transferWindow.quit(), transferWindow.destroy(), TransferScreen.main(SignInWindow.username, loadInput, UnloadContainersScreen.containers_list)]) # printAllContainers()

    # EXIT BUTTON
    exitBut = tk.Button(transferWindow, text = "Exit", command = transferWindow.destroy)

    transferLabel.pack(pady=5)
    loadBut.pack()
    unloadBut.pack()
    beginOrderBut.pack()
    exitBut.pack(pady=10)

    transferWindow.mainloop()

def printAllContainers():
    print('\n CONTAINERS TO LOAD: ')
    for i in loadInput:
        print(i)

    print('\n CONTAINERS TO UNLOAD: ')
    for i in UnloadContainersScreen.containers_list:
        print(i)

# LOAD WINDOW 
def loadWin():
    TRANSFER = True
    global loadWindow
    loadWindow = tk.Toplevel()
    loadWindow.title("Load Containers")
    loadWindow.geometry("300x200")
    containerLoadLabel = tk.Label(loadWindow, text = "Enter the containers to load:")
    entry = tk.Entry(loadWindow, textvariable = name_var, fg="Black", bg="white", width=200)
    enterBut =tk.Button(loadWindow, text= "Enter",width= 20, command= lambda: [appendLoadContainer(name_var), entry.delete(0, END)])
    
    
    doneButton = tk.Button(loadWindow, text = "Done", command=lambda: loadWindow.destroy())
   
    containerLoadLabel.pack(pady=(5,1))
    entry.pack(pady=5)
    enterBut.pack(pady=5)
    doneButton.pack(pady=5)
    

    loadWindow.mainloop()


def main():
    global TRANSFER
    TRANSFER = False
    
    global BALANCE
    BALANCE = False

    print("Before main menu TRANSFER is", TRANSFER)
    print("Before main menu BALANCE is", BALANCE)

    mainMenu()
    # username = saveUsername()
    # print("hellooo", username)

if __name__ == '__main__':
    main()
    
    
    