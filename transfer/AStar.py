from queue import PriorityQueue
import copy
# import sys

from basicgrid import createBasic
from printgrid import printGrid
from calcMH import calcTotalMH
from modifyGrid import modifyGrid
from goalState import isGoalState
import createGrid
import expandMoves

class PriorityEntry(object):
    def __init__(self, priority, data):
        self.data = data
        self.priority = priority
    def __lt__(self, other):
        return self.priority < other.priority
    def getData(self):
        return self.data

filename = "ShipCase5"

v = createBasic()
v = modifyGrid(v, filename)
offContainers = ["Hen", "Pig"]
loadContainers = ["Nat", "Rat"]
start = createGrid.newGrid(v, 0, offContainers, loadContainers, "", None, "")

# print("INITIAL STATE:")
# printGrid(createGrid.newGrid.getGrid(start))
# print("Initial MH is: ", calcTotalMH(start.getGrid(), offContainers, loadContainers, False))

finished = False

solution = None

# printnum = 0

pq = PriorityQueue()
pq.put(PriorityEntry((start.getDepth() + calcTotalMH(start.getGrid(), offContainers, loadContainers, False)), start))

hmap = {}
hmap[createGrid.newGrid.calcHash(start)] = None

while pq:
    # print("node number ", printnum)
    # printnum += 1
    node = pq.get()
    curr = node.getData()
    if isGoalState(createGrid.newGrid.getGrid(curr), createGrid.newGrid.getOffContainers(curr), createGrid.newGrid.getLoadContainers(curr), createGrid.newGrid.getIsGrabbing(curr)):
        solution = node
        break
    nodes = expandMoves.expandMoves(curr)
    for n in nodes:
        tempMH = createGrid.newGrid.getDepth(n) + calcTotalMH(createGrid.newGrid.getGrid(n), createGrid.newGrid.getOffContainers(n), createGrid.newGrid.getLoadContainers(n), createGrid.newGrid.getIsGrabbing(n))
        hash = createGrid.newGrid.calcHash(n)
        if hash not in hmap:
            hmap[hash] = None
            createGrid.newGrid.setParentNode(n, curr)
            pq.put(PriorityEntry(tempMH, n))

#priorityentry BS taken from https://stackoverflow.com/questions/40205223/priority-queue-with-tuples-and-dicts



if(solution):
    print("Solution found")
    # printInstructions(solution)
    currNode = solution.getData()
    finalNode = currNode
    newGrab = False
    containerPos = -1
    containerName = ""
    stack = []
    stackNames = []
    output = []
    finalDepth = createGrid.newGrid.getDepth(finalNode)
    while currNode:
        # printGrid(createGrid.newGrid.getGrid(currNode))
        if(createGrid.newGrid.getAction(currNode) == "grab"):
            if(newGrab == False):
                newGrab = True
                #get coordinates of container the crane is grabbing
                for cell in range(390):
                    if createGrid.newGrid.getGrid(currNode)[cell][1] == "CRANE":
                        containerPos = cell - 39
                #append cell position
                row = (containerPos // 39)
                fRow = row + 1
                col = (containerPos - ((row) * 39)) - 26
                if col == -1:
                    depthObj = finalDepth - createGrid.newGrid.getDepth(currNode)
                    stack.append(str(depthObj) + "(99,99)")
                elif col < 10:
                    depthObj = finalDepth - createGrid.newGrid.getDepth(currNode)
                    Str = "(0" + f'{fRow}' + ",0" + f'{col}' + ")"
                    stack.append(str(depthObj) + Str)
                else:
                    depthObj = finalDepth - createGrid.newGrid.getDepth(currNode)
                    Str = "(0" + f'{fRow}' + "," + f'{col}' + ")"
                    stack.append(str(depthObj) + Str)
        elif(createGrid.newGrid.getAction(currNode) == "release"):
            for cell in range(390):
                if createGrid.newGrid.getGrid(currNode)[cell][1] == "CRANE":
                    containerPos = cell - 39
            containerName = createGrid.newGrid.getGrid(currNode)[containerPos][1]
            row = (containerPos // 39)
            fRow = row + 1
            col = (containerPos - ((row) * 39)) - 26
            if col == -1:
                stack.append("(99,99)")
                stackNames.append(containerName)
            elif col < 10:
                Str = "(0" + f'{fRow}' + ",0" + f'{col}' + ")"
                stack.append(Str)
                stackNames.append(containerName)
            else:
                Str = "(0" + f'{fRow}' + "," + f'{col}' + ")"
                stack.append(Str)
                stackNames.append(containerName)
            newGrab = False
        currNode = createGrid.newGrid.getParentNode(currNode)
    while stack:
        Str = stack.pop() + stack.pop() + " " + stackNames.pop()
        output.append(Str)
    finalOutput = []
    for i in range(len(output)):
        firstParen = output[i].index("(")
        remainingDepth = output[i][:firstParen]
        fromLoc = output[i][firstParen:firstParen+7]
        toLoc = output[i][firstParen+7:firstParen+14]
        cName = output[i][firstParen+15:]
        # print(remainingDepth, " ", fromLoc, " ", toLoc, " ", cName, "asdf", sep="")
        mins = int(remainingDepth)
        hours = mins // 60
        days = hours // 24
        hours = hours % 24
        mins = mins % 60
        if(fromLoc == "(99,99)"):
            Str = fromLoc + toLoc + " [LOAD] " + "<" + f'{days:02}' + ":" + f'{hours:02}' + ":" + f'{mins:02}' + "> " + cName
            finalOutput.append(Str)
            # print(str)
        elif(toLoc == "(99,99)"):
            Str = fromLoc + toLoc + " [OFFLOAD] " + "<" + f'{days:02}' + ":" + f'{hours:02}' + ":" + f'{mins:02}' + "> " + cName
            finalOutput.append(Str)
        else:
            Str = fromLoc + toLoc + " [MOVE WITHIN SHIP] " + "<" + f'{days:02}' + ":" + f'{hours:02}' + ":" + f'{mins:02}' + "> " + cName
            finalOutput.append(Str)
            # converting single digits to double digits from stackoverflow: https://stackoverflow.com/questions/3505831/in-python-how-do-i-convert-a-single-digit-number-into-a-double-digits-string (multiple commentors)
    f = open(filename + "GUIPathOutput.txt", "w")
    f.write(finalOutput.pop(0))
    while finalOutput:
        f.write("\n")
        f.write(finalOutput.pop(0))
    f.close()
    # stack and queue from geeksforgeeks
else:
    print("No solution found")