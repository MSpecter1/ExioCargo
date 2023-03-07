import tkinter as tk
import time

root = tk.Tk()
running = True

shipGrid = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # row 0
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # row 1
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # row 2
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # row 3
                [0, 0, 0, 0, 0, 0, "GREEN", 0, 0, 0, 0, 0], # row 4
                [0, 0, 0, 0, 0, 0, "RED", 0, 0, 0, 0, 0], # row 5
                ["NAN", 0, "BLUE", 0, 0, "GREEN", "BLUE", 0, 0, 0, 0, "NAN"], # row 6
                ["NAN", "NAN", "RED", "ORANGE", 0, "BLUE", "GREEN", 0, 0, "RED", "NAN", "NAN"] # row 7                
                ]

# class Container: 
#     def __init__(self, name, weight, button):
#        self.name = name #h should be set to 0 for Uniform Cost Search
#        self.weight = weight #depth of the node
#        self.button =  tk.Button(root, text="", height=5, width=10, bg='white',activebackground='lightgrey', command=lambda row=i, column=j: print(row, column))

timer = 150
# Define a function to start the loop
def on_start():
   global running
   running = True

# Define a function to stop the loop
def on_stop():
   global running
   running = False

button_grid = []
def buildShipGrid(shipGrid): #building a dummy grid
    for i in range(8):
        button_row = []
        for j in range(12):

            if(shipGrid[i][j] == 0): #0 means "UNUSED"
                button = tk.Button(root, text=f"({i},{j})", height=5, width=10, bg='white',activebackground='lightgrey', command=lambda row=i, column=j: print(row, column))
                button.grid(row=i, column=j)
                button_row.append(button)

            elif(shipGrid[i][j] == "NAN"):
                button = tk.Button(root, text="", height=5, width=10, bg='black',activebackground='black', command=lambda row=i, column=j: print(row, column))
                button.grid(row=i, column=j)
                button_row.append(button)

            else:
                button = tk.Button(root, text=shipGrid[i][j] + f"({i},{j})", height=5, width=10, bg='blue',activebackground='lightgrey', command=lambda row=i, column=j: print(row, column))
                button.grid(row=i, column=j)
                button_row.append(button)

        button_grid.append(button_row)

def computeRow(y):
    return y + ((-2 * y) + 8)

def computeCol(x):
    return x-1

def maxY(slot1, slot2):
    slot1_row, slot1_col = slot1
    print("slot1's row:", slot1_row)
    print("slot1's col:", slot1_col)

    slot2_row, slot2_col = slot2
    print("slot2's row:", slot2_row)
    print("slot2's col:", slot2_col)

    #Condition 1: move left to right; if slot1_col < slot2_col
    if slot1_col < slot2_col:
        print("Condition 1")
        maxRow = 100
        for c in range(slot1_col, slot2_col+1): # moving horizontally X
            for r in range(slot2_row, -1, -1): # moving vertically Y
                # print(button_grid[r][c].cget('bg'), r, c)
                if(button_grid[r][c].cget('bg') != "white" and button_grid[r][c].cget('bg') != "black"): #Find the max Y or row; decrements from slot1's row to the top/0th row
                    # print(button_grid[r][c].cget('bg'), r, c)
                    if(r < maxRow):
                        maxRow = r
                        # print(maxRow)
        moveUp = maxRow-1

    #TODO: Condition 2: move right to left; if slot1_col > slot2_col // here, instead of incrementing the c/col we, decrement it up to slot2_col
    if slot1_col > slot2_col: 
        print("Condition 2")
        maxRow = 100
        for c in range(slot1_col, slot2_col-1, -1): # moving horizontally X
            for r in range(slot2_row, -1, -1): # moving vertically Y
                # print("r,c", r, c)
                if(button_grid[r][c].cget('bg') != "white" and button_grid[r][c].cget('bg') != "black"): #Find the max Y or row; decrements from slot1's row to the top/0th row
                    # print(button_grid[r][c].cget('bg'), r, c)
                    if(r < maxRow):
                        maxRow = r
                        # print(maxRow)
        moveUp = maxRow-1


    if(moveUp == 99): #if it's all white space and no containers are blocking in between, just set the max height to row2's row value
        moveUp = slot2_row
    
    print("Max height/row:", moveUp)
    return moveUp

def animateUp(y, slot1): # combine animateDown here 
    row, col = slot1
    print("y, row, col", y, row, col)

    # while True: #
    for i in range(row-1, y, -1): # i > y ; onlu up to y to avoid double counting/lighting the maxY button for animateUp
        # print('enter')
        # prevButton = button_grid[i][col]
        lightButton = button_grid[i][col]
        lightButton.config(bg="light sky blue")
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
        print("Condition 1: moveRight")
        for i in range(slot1_col, slot2_col+1):
            lightButton = button_grid[moveMaxHeight][i]
            lightButton.config(bg="light sky blue")
            lightButton.update()
            root.after(timer)
            lightButton.config(bg="white")
            lightButton.update()
            root.after(timer)

    # Condition 2: move right to left; if slot1_col > slot2_col
    if slot1_col > slot2_col:
        print("Condition 2: moveLeft")
        for i in range(slot1_col, slot2_col-1, -1):
            lightButton = button_grid[moveMaxHeight][i]
            lightButton.config(bg="light sky blue")
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
        lightButton.config(bg="light sky blue")
        lightButton.update()
        root.after(timer)
        lightButton.config(bg="white")
        lightButton.update()
        root.after(timer)
    
def updateNextGrid(slot2): # updates the 8x12 grid to reflect the current step's move/task has been completed once the user presses "Next"
    slot2_row, slot2_col = slot2

    updateSlot2Button = button_grid[slot2_row][slot2_col]
    updateSlot2Button.config(bg="blue")
    updateSlot2Button.update()

def main():
    buildShipGrid(shipGrid)
    button = tk.Button(root, text="Next",activebackground='lightgrey', height=1, width=8, command=on_stop)
    button.grid(row=9, column=6)
    # (row, col) => (y, x)
    # Move container from (2, 3) to (2, 10) => (6, 2) to (6, 9)
    # manifest/ship coord (a,b): (2,3) --> UI_X =  a + (-2a + 8), UI_Y = b - 1

    # pair1 = (2, 10) # (2, 3)
    # pair2 = (3, 12) # (2, 10)

    pair1 = (2, 3)
    pair2 = (2, 10)

    pair1R, pair1C = pair1
    pair2R, pair2C = pair2
    print("pair1", pair1R, pair1C)
    print("pair2", pair2R, pair2C)

    slot1_row = computeRow(pair1R) # 6
    slot1_col = computeCol(pair1C) # 2
    slot1 = (slot1_row, slot1_col)

    slot2_row = computeRow(pair2R) # 6
    slot2_col = computeCol(pair2C) # 9
    slot2 = (slot2_row, slot2_col)
    print(f"Moving container from {slot1} to {slot2}")


    moveMaxHeight = maxY(slot1, slot2)
    moveMaxDown = maxDown(slot2, moveMaxHeight)
    print(moveMaxDown)


    while True:
        animateUp(moveMaxHeight, slot1)
        # root.after(timer)
        animateHorizontal(slot1, slot2, moveMaxHeight)
        animateDown(slot2, moveMaxHeight, moveMaxDown)
        if running == False:  #add condition for when user hits "Next", stop the loop so it can go to next step's new animation
            break       
    
    updateNextGrid(slot2)
    print("Broke out of animation loop!") #break out of loop
    root.mainloop()

if __name__ == '__main__':
    main()

#TODO 1: perform some conversion that takes Michael's (col, row) coordinates and then converts it to Manifest's coordinate format
#TODO 2: create a function that reads in a Manifest text file to create the 8x12 2D array named "shipGrid" 
#TODO 3: add a grid for displaying the buffer (can probably just do this in main() or outside main())

'''
PLAN for function buildShipGrid(): use position in matrix (x, y) as the unique ID for each slot <-- will update this function buildShipGrid() once manifest reader is finalized or try asking them tmrw about it

1) Take in 2D array generated from Alex or Michael's manifest reader. I believe it should be a 2D array of container objects (with attributes for the name and weight)
2) Take in my button array. Loop through button array/grid and for each slot (i and j or (x,y) position), 
    if buttonArray[i][j] == manifestArray[i][j]: 
        GET manifestArray[i][j].name and set the buttonArray[i][j]'s or tk.Button(root, text="", ...) the text= manifestArray[i][j].name
'''