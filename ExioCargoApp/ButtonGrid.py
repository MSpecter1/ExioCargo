import tkinter as tk
from tkinter import *
import ntplib
from time import ctime
import sys
import os
import SignInWindow
# adding UnloadProblem to system path
import Balance
# import menu
import numpy as np
import MainMenu
from tktooltip import ToolTip
import pathlib 
from tkinter.tix import *
from tkinter import tix

global USER
# USER = MainMenu.MainMenuUser

def assignManifest(f):
    global manifest_filepath
    manifest_filepath = f

def balanceStartUp():
    global root
    root = tix.Tk()

    root.state("zoomed") # when window opens, it fills up whole screen

    global frame
    frame = Frame(root)
    frame.pack(side=LEFT, pady=20)
    
    global ship_bg_frame
    ship_bg_frame = Frame(frame, bg="grey")  #
    ship_bg_frame.pack(side=TOP, expand=1)

    global ship_frame
    ship_frame = Frame(ship_bg_frame, bg="white")
    ship_frame.pack(side=LEFT, expand=1, padx=10, pady=10)

    global nextButton_bg_frame
    nextButton_bg_frame = Frame(frame, bg="light grey")  #
    nextButton_bg_frame.pack(side=BOTTOM, expand=1, fill=X)

    global nextButton_frame
    nextButton_frame = Frame(nextButton_bg_frame)#ship_bg_frame
    nextButton_frame.pack(side=BOTTOM, pady=10)

    # Top Right Frame
    global frameTopRight
    frameTopRight = Frame(root, width=700, height=500,bg="grey")
    frameTopRight.pack(side=TOP, padx=10, pady=20)

    global logCommentLabel
    logCommentLabel = Label(frameTopRight,
                    text = "Log Comment", bg="grey", fg="white",font=("Cambria", 12, "bold")).place(x=3, y=200)
    
    global logCommentEntry
    logCommentEntry = tk.Entry(frameTopRight, width=30)        # logCommentEntry = Text(frameTopRight, width=30, height=8).place(x=110, y=80) 
    logCommentEntry.place(x=110, y=204) 

    global logSubmitComment
    logSubmitComment = Button(frameTopRight,text="Submit Comment", command=getLogComment).place(x=300, y=201)  # Button(frameTopRight,text="Submit").place(x=215, y=213)

    global signInButton
    # LOG EVENT: UserSwitch; need to log this to the Log File
    signInButton = Button(frameTopRight,text="Sign In", command=lambda: [signInWin()])
    signInButton.place(x=530, y=13)  # Button(frameTopRight,text="Submit").place(x=215, y=213)
    # Button goes back to the MAIN MENU

    global mainMenuButton
    mainMenuButton = Button(frameTopRight,text="Exit to Main Menu", command=lambda:[root.quit(), root.destroy(), MainMenu.main()])
    mainMenuButton.place(x=585, y=13)  # Button(frameTopRight,text="Submit").place(x=215, y=213)

    # Bottom Right Frame 
    global frameBotRight
    frameBotRight= Frame(root, width=500, height=500,bg="grey")
    frameBotRight.pack(side=TOP, padx=10, pady=20)

    global buffer_frame
    buffer_frame = Frame(frameBotRight, bg="light grey") #ship_bg_frame
    buffer_frame.pack(side=TOP, expand=1,padx=4,pady=5) #RIGHT

    global bufferLabel
    bufferLabel = Label(frameBotRight,  text = "BUFFER", font=("Cambria", 12, "bold"))
    bufferLabel.pack(pady=5)

    return ship_frame

global running
running = True

timer = 150
path_arr = []

# Define a function to start the loop
def on_start():
   global running
   running = True

# Define a function to stop the loop
def on_stop():
   global running
   running = False

def getLogComment():
    # print("LOG COMMENT SUBMITTED", logCommentEntry.get())
    comment = logCommentEntry.get()
    logCommentEntry.delete(0, END)

    # LOG EVENT: LogComment; need to log this to the Log File
    # For Log Comments: (LogComment, Date & Time the log comment was submitted, Operator's Log Comment) 
    if comment != "":
        addLogEvent(("LogComment", getDateTime(), comment))
    return comment

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

global log_events_arr
log_events_arr = []
def addLogEvent(logObj):
    print("Added event to log event array", logObj)
    log_events_arr.append(logObj)

def updateLogFile():
    f = open("KeoghLongBeach2023.txt", "a")
    print("start updateLogFile()")
    for event in log_events_arr:
        line = ""
        eventType = event[0]
        # print(eventType)

        currentDateTime = event[1]
        
        if eventType == "LogComment" or eventType == "CycleComplete":
            description = event[2]
            line = currentDateTime + description + "\n"
            f.write(line)
            print(line)
        elif eventType == "UserSwitch":
            signOut = event[2]
            signIn = event[3] 
            line = currentDateTime + signOut + "\n" # line for signout
            print(line)
            f.write(line)
            
            line = currentDateTime + signIn + "\n" #line for signin
            print(line)
            f.write(line)

def signInWin():
    global USER
    SignInWindow.startUp()
    
    USER = SignInWindow.username
    userLabel.config(text=f"User: {USER}")
    
    addLogEvent(("UserSwitch", getDateTime(), f"{SignInWindow.pastUser} signs out", f"{USER} signs in"))
    SignInWindow.pastUser = SignInWindow.username
    print("test USER", USER)
    

''' MAIN ANIMATION CODE BEGINS HERE '''
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class container:
    def __init__(self, name, x, y, weight, frame):
        self.name = name
        self.x = x
        self.y = y
        self.weight = weight
        self.frame = frame
        self.tip = Balloon(root)

        if(self.name == "UNUSED"):
                self.button = tk.Button(frame, text=name, height=4, width=7, bg='white',activebackground='lightgrey')
                

        elif(self.name == "NAN"):
                self.button = tk.Button(frame, text="NAN", height=4, width=7, bg='black',activebackground='black')

        else:
                self.button = tk.Button(frame, text=name, height=4, width=7, bg='#004fff',activebackground='lightgrey')
                

        self.tip.bind_widget(self.button, balloonmsg=f"{self.name}\n ({self.x}, {self.y}) \n Weight: {self.weight}")
        # ToolTip(self.button, msg=f"{self.name}\n ({self.x}, {self.y}) \n Weight: {self.weight}", follow=True) 

    def display_info(self):
        print("Position: [",self.x,",", self.y,"], Weight:", self.weight ,"kg, Name:",self.name)

    def getName(self):
        return self.name


def read_manifest(file, frame):
        containers = []
        with open(file) as f:
            # Per line
            while True:
                line = f.readline()
                if not line:
                    break
                line=line.strip()
                # X
                x=int(line[1:3]) 
                # Y
                y=int(line[4:6])
                # Weight - kilograms
                w=int(line[10:15])
                # Name
                n=(line[18:])
                # create container
                containers.append(container(n,x,y,w, frame))

        return containers
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
buffer_grid = []
def createBuffer():
    for i in range(4):
        buffer_row = []
        for j in range(24):
            global button
            buffbutton = tk.Button(buffer_frame, font=("Arial", 7), height=3, width=3, bg='white')
            bufftip = Balloon(root)
            bufftip.bind_widget(buffbutton, balloonmsg=f"(row, column)\n({4-i},{j+1})")
            buffbutton.grid(row=i, column=j)
            buffer_row.append(buffbutton)
        buffer_grid.append(buffer_row)


def pathReader(): # reads Balance's GUI Path Output
    # Run the Balance algorithm to retrieve the path solutions array 
    searchOBJ = Balance.CargoSearch()
    stateOBJ = Balance.ShipState()
    returned_sol = searchOBJ.search(stateOBJ, manifest_filepath) 
    solution_paths = returned_sol.solution
    print(solution_paths)

    print("PATH READER")
    for path in solution_paths:
        # slot1's row
        slot1_row=int(path[1:3]) 
        # slot1's col
        slot1_col=int(path[4:6])

        #slot2's row
        slot2_row=int(path[8:10])
        #slot2's col
        slot2_col=int(path[11:13])

        est_time = int(path[15:19])

        # Name
        n=(path[20:])

        global slot1
        slot1 = (slot1_row, slot1_col)
        slot2 = (slot2_row, slot2_col)

        path_arr.append((slot1, slot2, n, est_time))
        print("slot1 row,col:", slot1, "// slot2 row,col:", slot2, "Name:", n, "est time:", est_time)

    for i in range(len(path_arr)):
        print(path_arr[i])

    global numSteps
    numSteps = len(solution_paths)
    print("Total number of steps:", numSteps)
    
    global totalTime
    totalTime = est_time
    print("Total Time:", totalTime)


button_grid = []

def buildShipGrid(frame):
    global manifestFile
    manifestFile = manifest_filepath
    global shipName
    
    path = pathlib.PurePath(manifest_filepath)
    txtFile = path.name
    file = txtFile.split(".txt")
    shipName = file[0]

    containers_arr = read_manifest(manifest_filepath, frame)
    global containers_2D
    containers_2D = list(np.reshape(containers_arr, (8,12)))

    containers_2D.reverse()
    for i in range(8):
        button_row = []
        for j in range(12):
            container = containers_2D[i][j]
            # print(f"({container.x}, {container.y})", container.weight, container.name, container.button.cget('text'))
            container.button.config(text=container.name, command=lambda row=i, column=j, container_x=container.x, container_y=container.y, container_weight=container.weight, container_name=container.name: print("row:", row, "column:", column, "ManifestX:", container_x, "ManifestY:", container_y, "Name:", container_name, "Weight:", container_weight))
            container.button.update()
            button = container.button
            button.grid(row=i, column=j)
            button_row.append(button)
        button_grid.append(button_row)

def computeRow(y):
    return y + ((-2 * y) + 8)

def computeCol(x):
    return x-1

def maxY(slot1, slot2):
    moveUp = -1
    slot1_row, slot1_col = slot1

    slot2_row, slot2_col = slot2

#if there's nothing obstructing the horizontal path between slot1 and slot2, then just move horizontally...
    # Condition 1: move left to right; if slot1_col < slot2_col
    if slot1_col < slot2_col:
        print("Condition 1")
        maxRow = slot1_row
        for c in range(slot1_col+1, slot2_col+1): # moving horizontally X
            for r in range(slot1_row, -1, -1): # moving vertically Y

                # print(r,c)
                if(button_grid[r][c].cget('bg') != "white" and button_grid[r][c].cget('bg') != "black"): #Find the max Y or row; decrements from slot1's row to the top/0th row
                    # print(button_grid[r][c].cget('bg'), r, c)
                    if(r <= maxRow):
                        maxRow = r
                        # row_start = maxRow
                        moveUp = maxRow-1
                        print("MAXX height/row:", maxRow)

    # Condition 2: move right to left; if slot1_col > slot2_col // here, instead of incrementing the c/col we, decrement it up to slot2_col
    if slot1_col > slot2_col: #TODO: TEST & FIX THIS NEXT
        print("Condition 2")
        maxRow = slot1_row
        for c in range(slot1_col-1, slot2_col-1, -1): # moving horizontally X
            for r in range(slot1_row, -1, -1): # moving vertically Y
                # print(r,c)
                if(button_grid[r][c].cget('bg') != "white" and button_grid[r][c].cget('bg') != "black"): #Find the max Y or row; decrements from slot1's row to the top/0th row
                    # print(button_grid[r][c].cget('bg'), r, c)
                    if(r <= maxRow):
                        maxRow = r
                        moveUp = maxRow-1  # move 1 up above current slot1 container
                        print("MAXX height/row:", maxRow)


    if moveUp == -1: # if nothing in the between slot1 and slot2 is found to be taller than either slot1 or slot2's height, just set it to slot1's height
        moveUp = slot1_row


    print("Max height/row:", moveUp)
    return moveUp

def animateUp(y, slot1, name): # combine animateDown here 
    row, col = slot1
    
    # while True: #
    for i in range(row-1, y, -1): # i > y ; only up to y to avoid double counting/lighting the maxY button for animateUp
        # print('enter')
        # prevButton = button_grid[i][col]
        lightButton = button_grid[i][col]
        lightButton.config(bg="cyan", text=name)
        lightButton.update()
        root.after(timer)
        lightButton.config(bg="white", text="UNUSED")
        lightButton.update()
        root.after(timer)


def animateHorizontal(slot1, slot2, moveMaxHeight, name):
    slot1_row, slot1_col = slot1
    slot2_row, slot2_col = slot2

    
    # Condition 1: move left to right; if slot1_col < slot2_col
    if slot1_col < slot2_col:

        if moveMaxHeight == slot1_row: #TEMPORARY POSSIBLY: for ShipCase4 case where the container being moved is on the very first row (which is already the maxHeight)
            slot1_col+=1
            # print("WAT", slot1_row, slot1_col)

        # print("Condition 1: moveRight")
        for i in range(slot1_col, slot2_col+1):
            lightButton = button_grid[moveMaxHeight][i]
            lightButton.config(bg="cyan", text=name)
            lightButton.update()
            root.after(timer)
            lightButton.config(bg="white", text="UNUSED")
            lightButton.update()
            root.after(timer)

    # Condition 2: move right to left; if slot1_col > slot2_col
    if slot1_col > slot2_col: 
        if moveMaxHeight == slot1_row: #TEMPORARY POSSIBLY: case where the container being moved is on the very first row (which is already the maxHeight), good example of this scenario is ShipCase4
            slot1_col-=1
            # print("WAT", slot1_row, slot1_col)
        # print("Condition 2: moveLeft")
        for i in range(slot1_col, slot2_col-1, -1):
            lightButton = button_grid[moveMaxHeight][i]
            lightButton.config(bg="cyan", text=name)
            lightButton.update()
            root.after(timer)
            lightButton.config(bg="white", text="UNUSED")
            lightButton.update()
            root.after(timer)

def maxDown(slot2, moveMaxHeight):
    slot2_row, slot2_col = slot2
    
    downLimit = 7
    for i in range(moveMaxHeight, 8): #move from maxHeight to last row to search for next blue/USED or black/NAN block
        if(button_grid[i][slot2_col].cget('bg') == "#004fff" or button_grid[i][slot2_col].cget('bg') == "black"):
                downLimit = i-1
                break # break out of loop once we find the first blue/USED or black/NAN block
    print("downLimit", downLimit)
    return downLimit


# stay in slot2_col, move down from moveMaxHeight to next below blue box in the same slot2_col column
# to find the next below blue box, start from moveMaxHeight then check for each box[i++][col]
def animateDown(slot2, moveMaxHeight, moveMaxDown, name):
    slot2_row, slot2_col = slot2

    for i in range(moveMaxHeight+1, moveMaxDown+1): # move animation from maxHeight to the maxDown (i.e. the first blue or black box maxHeight)
        lightButton = button_grid[i][slot2_col]
        lightButton.config(bg="cyan", text=name)
        lightButton.update()
        root.after(timer)
        lightButton.config(bg="white", text="UNUSED")
        lightButton.update()
        root.after(timer)

def updateToolTip(button, n, w, x, y, containerObj):
    # ToolTip(button, msg=f"{n}\n({x}, {y})\nWeight: {w}", follow=True) 
    containerObj.tip.destroy()
    newTip = Balloon(root)
    containerObj.tip = newTip
    newTip.bind_widget(button, balloonmsg=f"{n}\n({x}, {y})\nWeight: {w}")
    


def updateNextGrid(slot1, slot2): # updates the 8x12 grid to reflect the current step's move/task has been completed once the user presses "Next"
    slot1_row, slot1_col = slot1
    slot2_row, slot2_col = slot2

    updateSlot2Button = button_grid[slot2_row][slot2_col]
    slot2Container = containers_2D[slot2_row][slot2_col]
    slot1_name = containers_2D[slot1_row][slot1_col].name # assign slot1's name to slot2's button text and to update container_2D
    slot1_weight = containers_2D[slot1_row][slot1_col].weight # update container_2D's slot2 weight
    slot2Container.name = slot1_name
    slot2Container.weight = slot1_weight
    updateSlot2Button.config(bg="#004fff", text=slot1_name)
    updateSlot2Button.update()
    updateToolTip(updateSlot2Button, slot2Container.name, slot2Container.weight, slot2Container.x, slot2Container.y, slot2Container)
    

    updateSlot1Button = button_grid[slot1_row][slot1_col]
    slot1Container = containers_2D[slot1_row][slot1_col]
    slot1Container.name = "UNUSED"
    slot1Container.weight = 0
    updateSlot1Button.config(bg="white", text="UNUSED")
    updateSlot1Button.update()
    updateToolTip(updateSlot1Button, slot1Container.name, slot1Container.weight, slot1Container.x, slot1Container.y, slot1Container)

def popUpWindow():
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    popUp = tk.Toplevel()
    popUp.title("Email Outbound Manifest Reminder")
    w = popUp.winfo_width()
    h = popUp.winfo_height()  
    popUp.geometry("%dx%d+%d+%d" % (w, h, root_x+400, root_y+260))
    popUp.geometry("750x300")
    # popUpFrame = Frame(popUp)
    # popUpFrame.pack(side=TOP, pady=100) #350
    descriptionLabel = tk.Label(popUp, text = f"Manifest '{shipName}OUTBOUND.txt' was written to desktop.\n Make sure to send the file to the ship's captain.", font=("Cambria", 12, "bold"))
    exitButton = tk.Button(popUp, text = "Exit", width=10, height=1, command = popUp.destroy)
    descriptionLabel.pack(pady=60)
    exitButton.pack()

def exportOutboundManifest():
    filename = shipName
    print(os.environ['USERPROFILE'])
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    print(desktop)
    f = open(desktop+f"\{filename}"+"OUTBOUND.txt", "w")
    print(desktop+f"\{filename}"+"OUTBOUND.txt")
    for j in range(7,-1,-1): 
        for i in range(12):
            c = containers_2D[j][i]
            f.write('['+str("%02d"%(c.x))+','+str("%02d"%(c.y))+'], {'+str("%05d"%c.weight)+'}, '+str(c.name)+'\n') 

def main(user_name):
    USER = user_name
    ship_fr = balanceStartUp()
    buildShipGrid(ship_fr)    
    createBuffer()
    button = tk.Button(nextButton_frame, text="Next",activebackground='lightgrey', height=1, width=8, command=on_stop)
    button.grid(row=0, column=0)
    # (row, col) => (y, x)
    # Move container from (2, 3) to (2, 10) => (6, 2) to (6, 9)
    # manifest/ship coord (a,b): (2,3) --> UI_X =  a + (-2a + 8), UI_Y = b - 1

    # pair1 = (2, 3)
    # pair2 = (2, 10)

    pathReader()
    
    # path_arr = []
    # path_arr.append((pair1, pair2, "hello")) #DELETE THIS AFTER TESTING
    # path_arr.append(())
    global userLabel
    userLabel = Label(frameTopRight, text = f"User: {USER}", bg="grey",fg="white", font=("Cambria", 10, "bold"))
    userLabel.place(x=0, y=0)
    for i in range(len(path_arr)):
        print("\n\nSTEP", i, path_arr[i])
        stepsLabel = Label(frameTopRight, text = f"STEP {i+1} OF {numSteps}", bg="grey",fg="white", font=("Cambria", 14, "bold"))
        stepsLabel.place(x=295, y=60) 
        operationLabel = Label(frameTopRight, text = f"Move container {path_arr[i][2]} from {path_arr[i][0]} to {path_arr[i][1]}", bg="grey",fg="white",font=("Cambria", 14, "bold"))
        operationLabel.place(x=175, y=114)
        if(i == 0):
            curr_time = totalTime
        else:
            curr_time = totalTime - path_arr[i-1][3]
        estimatedTimeLabel = Label(frameTopRight, text = f"Estimated Time Left: {curr_time} minutes", bg="grey", fg="white", font=("Cambria", 14, "bold"))
        estimatedTimeLabel.place(x=210, y=87) 
        slot1R, slot1C = path_arr[i][0]
        slot2R, slot2C = path_arr[i][1]
        name = path_arr[i][2]

        slot1_row = computeRow(slot1R) 
        slot1_col = computeCol(slot1C) 
        slot1 = (slot1_row, slot1_col)

        slot2_row = computeRow(slot2R) 
        slot2_col = computeCol(slot2C) 
        slot2 = (slot2_row, slot2_col)

        print(f"Moving container {name} from {slot1} to {slot2}")


        moveMaxHeight = maxY(slot1, slot2)
        moveMaxDown = maxDown(slot2, moveMaxHeight)

        while True:
            print(USER)
            animateUp(moveMaxHeight, slot1, name)
            # root.after(timer)
            animateHorizontal(slot1, slot2, moveMaxHeight, name)
            animateDown(slot2, moveMaxHeight, moveMaxDown, name)
            if running == False:  #add condition for when user hits "Next", stop the loop so it can go to next step's new animation
                updateNextGrid(slot1,slot2)
                on_start()
                break
        
    # LOG EVENT: Cycle Completed; need to log this to the Log File
    # FORMAT: (CycleComplete, Date & Time, "Manifest <ship name> was written to desktop, and a reminder pop-up to operator to send file was displayed." )
    popUpWindow() # pop-up window for reminding the operator to email the new manifest to the ship's captain
    estimatedTimeLabel.config(text=f"Estimated Time Left: 0 minutes")
    stepsLabel.config(text="Cycle complete!")
    operationLabel.config(text="Select 'Exit to Main Menu' to begin a new cycle.")
    addLogEvent(("CycleComplete", getDateTime(), f"Finished a Cycle. Manifest {shipName}OUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed." ))
    updateLogFile()
    exportOutboundManifest()
    print("Broke out of animation loop!") #break out of loop
    
    root.mainloop()

if __name__ == '__main__':
    main("DEFAULT")