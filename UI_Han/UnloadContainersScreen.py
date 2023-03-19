import tkinter as tk
from tkinter import *
import numpy as np

root = tk.Tk()
root.state("zoomed")

# LEFT FRAME for 8x12 Grid
frame = Frame(root)
frame.pack(side=TOP, pady=75)

ship_bg_frame = Frame(frame, bg="grey")  #
ship_bg_frame.pack(side=TOP, expand=1)

ship_frame = Frame(ship_bg_frame, bg="white")
ship_frame.pack(side=LEFT, expand=1, padx=10, pady=10)

doneButton_bg_frame = Frame(frame, bg="light grey")  #
doneButton_bg_frame.pack(side=TOP, expand=1, fill=BOTH)

doneButton_frame = Frame(doneButton_bg_frame)#ship_bg_frame
doneButton_frame.pack(side=BOTTOM, expand=1, pady=10)
doneButton = Button(doneButton_frame, text="DONE", height=5, width=7, bg='white',activebackground='lightgrey')
doneButton.pack(side=TOP, expand=1)

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

        return containers
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
# Appending Containers to list
global containers_list
containers_list = []
def appendContainers(container, row, col):
    
    if(container.name != "UNUSED" and container.name != "NAN"):
        if(container.button.cget('bg') != "light grey"):
            container.button.config(bg="light grey") #on select, color selected container grey 
            containers_list.append(container)
            print("\nAPPENDED CONTAINER:", container.name, container.x, container.y)
            printContainerList()
        else:
             container.button.config(bg="blue")
             deleteContainer(container)
    
    

# Delete container from list if User selects on a greyed out button
def deleteContainer(container):
     print("\nDELETE CONTAINER:", container.name, container.x, container.y)
     containers_list.remove(container)
    #  print("len", len(containers_list))
     printContainerList()

def printContainerList(): #just for debugging purposes
    global text
    print("printing current list:")
    for i in range(len(containers_list)):
        container = containers_list[i]
        print(container.name, container.x, container.y)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------  

button_grid = []
containers_arr = read_manifest("Balance\ShipCase2.txt")
global manifestFile
manifestFile = "Balance\ShipCase1.txt"
global shipName
shipName = manifestFile.split("\\")[-1].split(".")[0]

def buildShipGrid():
    global containers_2D
    containers_2D = list(np.reshape(containers_arr, (8,12)))

    containers_2D.reverse()
    for i in range(8):
        button_row = []
        for j in range(12):
            container = containers_2D[i][j]
            container.button.config(text=container.name + f"\n({i},{j})", command=lambda row=i, column=j, container=container, container_x=container.x, container_y=container.y, container_weight=container.weight, container_name=container.name: [appendContainers(container, row, column)])
            container.button.update()
            button = container.button
            button.grid(row=i, column=j)
            button_row.append(button)
        button_grid.append(button_row)

def getLoadContainerList():
     return containers_list

def main():
    buildShipGrid()
    
if __name__ == '__main__':
    main()
    root.mainloop()
