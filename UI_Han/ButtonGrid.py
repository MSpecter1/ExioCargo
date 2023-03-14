import tkinter as tk
from tkinter import *
import ntplib
import time
import Balance
# import GUIManifestReader
import numpy as np

root = tk.Tk()
# root.attributes('-fullscreen', True)
root.state("zoomed") # when window opens, it fills up whole screen
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

# Left Frame
frame = Frame(root)
frame.pack(side=LEFT, pady=20)

ship_bg_frame = Frame(frame, bg="grey")  #
ship_bg_frame.pack(side=TOP, expand=1)

ship_frame = Frame(ship_bg_frame, bg="white")
ship_frame.pack(side=LEFT, expand=1, padx=10, pady=10)

nextButton_bg_frame = Frame(frame, bg="light grey")  #
nextButton_bg_frame.pack(side=BOTTOM, expand=1, fill=X)

nextButton_frame = Frame(nextButton_bg_frame)#ship_bg_frame
nextButton_frame.pack(side=BOTTOM, pady=10)


# buffer_frame = Frame(frame, bg="light grey") #ship_bg_frame
# buffer_frame.pack(side=TOP, expand=1,padx=4,pady=10) #RIGHT



# frameForRight = Frame(frameRight, bg="pink")
# frameForRight.pack(side=TOP, expand=1)

# Top Right Frame
frameTopRight = Frame(root, width=700, height=500,bg="grey")
frameTopRight.pack(side=TOP, padx=10, pady=20)

# frameForRight = Frame(frameRight, bg="pink")
# frameForRight.pack(side=TOP, expand=1)

logCommentLabel = Label(frameTopRight,
                  text = "Log Comment").place(x=20, y=120)
logCommentEntry = Entry(frameTopRight, width=30).place(x=110, y=120)         # logCommentEntry = Text(frameTopRight, width=30, height=8).place(x=110, y=80) 
logCommentSubmit = Button(frameTopRight,text="Submit Comment").place(x=300, y=120)  # Button(frameTopRight,text="Submit").place(x=215, y=213)

# Bottom Right Frame 
frameBotRight= Frame(root, width=500, height=500,bg="pink")
frameBotRight.pack(side=TOP, padx=10, pady=20)
buffer_frame = Frame(frameBotRight, bg="light grey") #ship_bg_frame
buffer_frame.pack(side=TOP, expand=1,padx=4,pady=5) #RIGHT


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class container:
    def __init__(self, name, x, y, weight):
        self.name = name
        self.x = x
        self.y = y
        self.weight = weight

        if(self.name == "UNUSED"):
                self.button = tk.Button(ship_frame, text=name, height=4, width=7, bg='white',activebackground='lightgrey')

        elif(self.name == "NAN"):
                self.button = tk.Button(ship_frame, text="NAN", height=4, width=7, bg='black',activebackground='black')

        else:
                self.button = tk.Button(ship_frame, text=name, height=4, width=7, bg='blue',activebackground='lightgrey')

    def display_info(self):
        print("Position: [",self.x,",", self.y,"], Weight:", self.weight ,"kg, Name:",self.name)

    def getName(self):
        return self.name


def read_manifest(file):
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
                containers.append(container(n,x,y,w))
        print(len(containers))
        # for i in range(len(containers)):
        #     print(containers[i].name, containers[i].weight)

        return containers
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
buffer_grid = []
def createBuffer():
    for i in range(4):
        buffer_row = []
        for j in range(24):
            global button
            buffbutton = tk.Button(buffer_frame, text=f"{j}", height=1, width=2, bg='white')
            buffbutton.grid(row=i, column=j)
            buffer_row.append(buffbutton)
        buffer_grid.append(buffer_row)


def pathReader(): # reads Balance's GUI Path Output
    # Run the Balance algorithm to retrieve the path solutions array 
    searchOBJ = Balance.CargoSearch()
    stateOBJ = Balance.ShipState()
    returned_sol = searchOBJ.search(stateOBJ, "Balance\ShipCase4.txt") 
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
containers_arr = read_manifest("Balance\ShipCase4.txt")
def buildShipGrid():
    global containers_2D
    containers_2D = list(np.reshape(containers_arr, (8,12)))

    containers_2D.reverse()
    for i in range(8):
        button_row = []
        for j in range(12):
            container = containers_2D[i][j]
            # print(f"({container.x}, {container.y})", container.weight, container.name, container.button.cget('text'))
            container.button.config(text=container.name + f"({i},{j})", command=lambda row=i, column=j, container_x=container.x, container_y=container.y, container_weight=container.weight, container_name=container.name: print("row:", row, "column:", column, "ManifestX:", container_x, "ManifestY:", container_y, "Name:", container_name, "Weight:", container_weight))
            container.button.update()
            button = container.button
            button.grid(row=i, column=j)
            button_row.append(button)
        button_grid.append(button_row)

    #check containers_2D before updateNextGrid() occurs
    print("containers_2D BEFORE UPDATE")
    for i in range(len(containers_2D)):
        print("ROW", i)
        for j in range(12):
            print("COL",j, containers_2D[i][j].button.cget('bg'), containers_2D[i][j].button.cget("text"), containers_2D[i][j].name, "weight:", containers_2D[i][j].weight, "row:", containers_2D[i][j].x, "col:", containers_2D[i][j].y)

def computeRow(y):
    return y + ((-2 * y) + 8)

def computeCol(x):
    return x-1

def maxY(slot1, slot2):
    moveUp = -1
    slot1_row, slot1_col = slot1
    print("slot1's row:", slot1_row)
    print("slot1's col:", slot1_col)

    slot2_row, slot2_col = slot2
    print("slot2's row:", slot2_row)
    print("slot2's col:", slot2_col)

    # row_start = slot1_row

#if there's nothing obstructing the horizontal path between slot1 and slot2, then just move horizontally...
    # Condition 1: move left to right; if slot1_col < slot2_col
    if slot1_col < slot2_col:
        print("Condition 1")
        maxRow = slot1_row
        for c in range(slot1_col+1, slot2_col+1): # moving horizontally X
            for r in range(slot1_row, -1, -1): # moving vertically Y

                print(r,c)
                if(button_grid[r][c].cget('bg') != "white" and button_grid[r][c].cget('bg') != "black"): #Find the max Y or row; decrements from slot1's row to the top/0th row
                    # print(button_grid[r][c].cget('bg'), r, c)
                    if(r <= maxRow):
                        maxRow = r
                        # row_start = maxRow
                        moveUp = maxRow-1
                        print("MAXX height/row:", maxRow)
                        
                # print("new start", row_start)

    # Condition 2: move right to left; if slot1_col > slot2_col // here, instead of incrementing the c/col we, decrement it up to slot2_col
    if slot1_col > slot2_col: #TODO: TEST & FIX THIS NEXT
        print("Condition 2")
        maxRow = slot1_row
        for c in range(slot1_col-1, slot2_col-1, -1): # moving horizontally X
            for r in range(slot1_row, -1, -1): # moving vertically Y
                print(r,c)
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

def animateUp(y, slot1): # combine animateDown here 
    row, col = slot1
    # print("y, row, col", y, row, col)
    
    # while True: #
    for i in range(row-1, y, -1): # i > y ; only up to y to avoid double counting/lighting the maxY button for animateUp
        # print('enter')
        # prevButton = button_grid[i][col]
        lightButton = button_grid[i][col]
        lightButton.config(bg="blue")
        lightButton.update()
        root.after(timer)
        lightButton.config(bg="white")
        lightButton.update()
        root.after(timer)


def animateHorizontal(slot1, slot2, moveMaxHeight):
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
            lightButton.config(bg="blue")
            lightButton.update()
            root.after(timer)
            lightButton.config(bg="white")
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
            lightButton.config(bg="blue")
            lightButton.update()
            root.after(timer)
            lightButton.config(bg="white")
            lightButton.update()
            root.after(timer)

def maxDown(slot2, moveMaxHeight):
    slot2_row, slot2_col = slot2
    
    downLimit = 7
    for i in range(moveMaxHeight, 8): #move from maxHeight to last row to search for next blue/USED or black/NAN block
        if(button_grid[i][slot2_col].cget('bg') == "blue" or button_grid[i][slot2_col].cget('bg') == "black"):
                downLimit = i-1
                break # break out of loop once we find the first blue/USED or black/NAN block
    print("downLimit", downLimit)
    return downLimit

# stay in slot2_col, move down from moveMaxHeight to next below blue box in the same slot2_col column
# to find the next below blue box, start from moveMaxHeight then check for each box[i++][col]
def animateDown(slot2, moveMaxHeight, moveMaxDown):
    slot2_row, slot2_col = slot2

    for i in range(moveMaxHeight+1, moveMaxDown+1): # move animation from maxHeight to the maxDown (i.e. the first blue or black box maxHeight)
        lightButton = button_grid[i][slot2_col]
        lightButton.config(bg="blue")
        lightButton.update()
        root.after(timer)
        lightButton.config(bg="white")
        lightButton.update()
        root.after(timer)

# TODO perform some updates on updateNextGrid() (information written below)!!!!!
def updateNextGrid(slot1, slot2): # updates the 8x12 grid to reflect the current step's move/task has been completed once the user presses "Next"
    slot1_row, slot1_col = slot1
    slot2_row, slot2_col = slot2

    updateSlot2Button = button_grid[slot2_row][slot2_col]
    slot2Container = containers_2D[slot2_row][slot2_col]
    slot1_name = containers_2D[slot1_row][slot1_col].name # assign slot1's name to slot2's button text and to update container_2D
    slot1_weight = containers_2D[slot1_row][slot1_col].weight # update container_2D's slot2 weight
    slot2Container.name = slot1_name
    slot2Container.weight = slot1_weight
    updateSlot2Button.config(bg="blue", text=slot1_name+f"({slot2_row},{slot2_col})")
    updateSlot2Button.update()

    updateSlot1Button = button_grid[slot1_row][slot1_col]
    slot1Container = containers_2D[slot1_row][slot1_col]
    slot1Container.name = "UNUSED"
    slot1Container.weight = 0
    updateSlot1Button.config(bg="white", text="UNUSED"+f"({slot1_row},{slot1_col})")
    updateSlot1Button.update()

    

def main():
    buildShipGrid()    
    createBuffer()
    button = tk.Button(nextButton_frame, text="Next",activebackground='lightgrey', height=1, width=8, command=on_stop)
    button.grid(row=0, column=0)
    # (row, col) => (y, x)
    # Move container from (2, 3) to (2, 10) => (6, 2) to (6, 9)
    # manifest/ship coord (a,b): (2,3) --> UI_X =  a + (-2a + 8), UI_Y = b - 1

    # pair1 = (2, 10) # (2, 3)
    # pair2 = (3, 12) # (2, 10)

    # pair1 = (1, 3)
    # pair2 = (1, 7)

    # pair1 = (8, 5)
    # pair2 = (2, 6)

    # pair1 = (2, 3)
    # pair2 = (2, 10)

    pathReader()
    
    # path_arr = []
    # path_arr.append((pair1, pair2, "hello")) #DELETE THIS AFTER TESTING
    # path_arr.append(())

    for i in range(len(path_arr)):
        print("\n\nSTEP", i, path_arr[i])
        stepsLabel = Label(frameTopRight, text = f"STEP {i+1} OF {numSteps}", bg="white", font=("Arial", 12)).place(x=285, y=13) 
        operationLabel = Label(frameTopRight, text = f"Move container {path_arr[i][2]} from {path_arr[i][0]} to {path_arr[i][1]}", bg="white",font=("Arial", 12)).place(x=205, y=70)
        if(i == 0):
            curr_time = totalTime
        else:
            curr_time = totalTime - path_arr[i-1][3]
        estimatedTimeLabel = Label(frameTopRight, text = f"Estimated Time Left: {curr_time} minutes", bg="white", font=("Arial", 12)).place(x=285, y=40) 
        slot1R, slot1C = path_arr[i][0]
        slot2R, slot2C = path_arr[i][1]
        name = path_arr[i][2]

        slot1_row = computeRow(slot1R) 
        slot1_col = computeCol(slot1C) 
        slot1 = (slot1_row, slot1_col)

        slot2_row = computeRow(slot2R) 
        slot2_col = computeCol(slot2C) 
        slot2 = (slot2_row, slot2_col)

        print("SLOT1", slot1, "; SLOT2", slot2)
        print(f"Moving container {name} from {slot1} to {slot2}")


        moveMaxHeight = maxY(slot1, slot2)
        moveMaxDown = maxDown(slot2, moveMaxHeight)
        print(moveMaxDown)


        while True:
            animateUp(moveMaxHeight, slot1)
            # root.after(timer)
            animateHorizontal(slot1, slot2, moveMaxHeight)
            animateDown(slot2, moveMaxHeight, moveMaxDown)
            if running == False:  #add condition for when user hits "Next", stop the loop so it can go to next step's new animation
                updateNextGrid(slot1,slot2)       # TODO: replace "break" with updateNextGrid(slot1,slot2) here
                on_start()
                break

        print("--containers_2D AFTER UPDATE")
        for i in range(len(containers_2D)):
            print("ROW", i)
            for j in range(12):
                print("COL",j, containers_2D[i][j].button.cget('bg'), containers_2D[i][j].button.cget("text"), containers_2D[i][j].name, "weight:", containers_2D[i][j].weight, "row:", containers_2D[i][j].x, "col:", containers_2D[i][j].y)
    
    print("Broke out of animation loop!") #break out of loop
    root.mainloop()

if __name__ == '__main__':
    main()

#TODO 1: add a grid for displaying the buffer (can probably just do this in main() or outside main())
#TODO 2: figure out how to make the animation stop immediately and go to the next grid (updateNextGrid()) when the user prints the "Next" button; right now, when the user presses the "Next" button, the animation has to finish its move first before updating to the next new grid/before (i.e. updateNextGrid) which is not very time-efficient
#TODO 3: make the containers different colors where there is a unique color for each container_name (question: do i have to consider the weight too? like if they two containers have the same name but different weights, do i color them differently or the same color?)

'''
ship_bg_frame = Frame(root, bg="grey", width=300, height=400)  #
ship_bg_frame.pack(side=TOP, expand=1)

ship_frame = Frame(ship_bg_frame, bg="white", width=400, height=400)
ship_frame.pack(side=LEFT, expand=1, padx=10, pady=10)

nextButton_bg_frame = Frame(root, bg="light grey", height=5, width=5)  #
nextButton_bg_frame.pack(side=BOTTOM, expand=1)

nextButton_frame = Frame(nextButton_bg_frame, bg="light grey", height=1, width=2)
nextButton_frame.pack(side=LEFT, padx=700, expand=1)

# buffer_bg_frame = Frame(root, bg="grey", width=300, height=300)  #
# buffer_bg_frame.pack(side=LEFT, expand=1)

buffer_frame = Frame(ship_bg_frame, bg="light grey")
buffer_frame.pack(side=RIGHT, padx=4)
# buffer_bg_frame = Frame(root, bg="grey", width=300, height=300)  #
# buffer_bg_frame.pack(side=LEFT, expand=1)

# buffer_frame = Frame(buffer_bg_frame, bg="light grey", height=300, width=300)
# buffer_frame.pack(side=LEFT, expand=1)
'''

