import tkinter as tk
from tkinter import *
import os
import sys
# sys.path.insert(0, 'UI_Han/BalanceProblem')
import ButtonGrid
import SignInWindow
import TransferScreen
import ButtonGrid

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
# MAIN MENU WINDOW (FIRST MENU)
def mainMenu():
    global menuRoot
    menuRoot = tk.Tk()
    menuRoot.geometry("700x400")
    # menuRoot.eval('tk::PlaceWindow . top')
    menuRoot.title("Main Menu")
    global name_var
    name_var=tk.StringVar()

    # TITLE
    mainMenuTitleLabel = Label(menuRoot, text= "Main Menu", bg='white', fg="black", font=("Cambria", 14, "bold"))

    # SIGN IN BUTTON
    signInButton = tk.Button(menuRoot,text="Sign In Here",width=25,height=2, bg="black", fg="white", command=lambda: [ SignInWindow.startUp(), assignPastUser()])
    
    
    # TRANSFER BUTTON
    transferButton = Button(menuRoot,text="Transfer",width=25,height=2,bg="blue",fg="yellow",command = transferWin) # opens the window for Transfer

    # BALANCE BUTTON
    balanceButton = tk.Button(menuRoot, text="Balance", width=25, height=2, bg="yellow", fg="blue", command=lambda: ButtonGrid.main(SignInWindow.username)) #runBalance()

    mainMenuTitleLabel.pack(pady=10) 
    signInButton.pack(pady=5)
    transferButton.pack(pady=5)
    balanceButton.pack(pady=5)
 
    menuRoot.mainloop() 

# TRANSFER PROBLEM WINDOW
def transferWin():
    global loadInput
    loadInput = []
    TRANSFER = True
    print("After TRANSFER is selected it is", TRANSFER)
    transferWindow = tk.Toplevel()
    transferWindow.title("TRANSFER")
    transferWindow.geometry("300x200")

    # TRANSFER TITLE
    transferLabel = tk.Label(transferWindow, text = "TRANSFER", bg='white', fg="black", font=("Cambria", 14, "bold"))
    
    # LOAD BUTTON
    loadBut = tk.Button(transferWindow,text="Load",width=25,height=2,bg="yellow",fg="blue",command = loadWin)

    # UNLOAD BUTTON
    unloadBut = tk.Button(transferWindow,text="Unload",width=25,height=2,bg="yellow",fg="red")

    # BEGIN ORDERING BUTTON
    beginOrderBut = tk.Button(transferWindow,text="Begin Ordering", width=25,height=2, bg="yellow",fg="green")

    # EXIT BUTTON
    exitBut = tk.Button(transferWindow, text = "Exit", command = transferWindow.destroy)

    transferLabel.pack(pady=5)
    loadBut.pack()
    unloadBut.pack()
    beginOrderBut.pack()
    exitBut.pack(pady=10)

    transferWindow.mainloop()

def sendLoadContainers():
    TransferScreen.main()
    loadWindow.destroy

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
    
    
    doneButton = tk.Button(loadWindow, text = "Done", command = lambda: sendLoadContainers())
   
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
    
    
    