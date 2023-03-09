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

v = createBasic()
v = modifyGrid(v)
offContainers = ["Cow"]
loadContainers = ["Bat", "Rat"]
# loadContainers = []
start = createGrid.newGrid(v, 0, offContainers, loadContainers, "", None)

print("INITIAL STATE:")
printGrid(createGrid.newGrid.getGrid(start))
print("Initial MH is: ", calcTotalMH(start.getGrid(), offContainers, loadContainers, False))

finished = False

solution = None

printnum = 0

pq = PriorityQueue()
pq.put(PriorityEntry((start.getDepth() + calcTotalMH(start.getGrid(), offContainers, loadContainers, False)), start))

# mh = start.getDepth() + calcTotalMH(start.getGrid(), offContainers, loadContainers)
hmap = {}
hmap[createGrid.newGrid.calcHash(start)] = None

while pq:
    # print("\n\n\n\n\n\n\n\n\n\n\n")
    print("node number ", printnum)
    printnum += 1
    node = pq.get()
    # print(type(node))
    curr = node.getData()
    # print("Previous move:")
    # print("MH of ", createGrid.newGrid.getDepth(curr) + calcTotalMH(createGrid.newGrid.getGrid(curr), createGrid.newGrid.getOffContainers(curr), createGrid.newGrid.getLoadContainers(curr), createGrid.newGrid.getIsGrabbing(curr)))
    # printGrid(createGrid.newGrid.getGrid(curr))
    # print("Possible moves:")
    # print(node.getData())
    if isGoalState(createGrid.newGrid.getGrid(curr), createGrid.newGrid.getOffContainers(curr), createGrid.newGrid.getLoadContainers(curr), createGrid.newGrid.getIsGrabbing(curr)):
        solution = node
        break
        # sys.exit()
    nodes = expandMoves.expandMoves(curr)
    for n in nodes:
        # pq.put((n.getDepth() + calcTotalMH(n.getGrid(), n.getOffContainers(), n.getLoadContainers)), n)
        tempMH = createGrid.newGrid.getDepth(n) + calcTotalMH(createGrid.newGrid.getGrid(n), createGrid.newGrid.getOffContainers(n), createGrid.newGrid.getLoadContainers(n), createGrid.newGrid.getIsGrabbing(n))
        hash = createGrid.newGrid.calcHash(n)
        if hash not in hmap:
            hmap[hash] = None
            createGrid.newGrid.setParentNode(n, curr)
            pq.put(PriorityEntry(tempMH, n))
            # if mh != tempMH:
            #     mh = tempMH
            # print("\nPutting the following grid with MH of ", tempMH, " into PQ:")
            # printGrid(createGrid.newGrid.getGrid(n))

#priorityentry BS taken from https://stackoverflow.com/questions/40205223/priority-queue-with-tuples-and-dicts

if(solution):
    print("Solution found")
    # printInstructions(solution)
    currNode = solution.getData()
    while currNode:
        printGrid(createGrid.newGrid.getGrid(currNode))
        currNode = createGrid.newGrid.getParentNode(currNode)
else:
    print("No solution found :(")


# v[178] = [178, "asdklf"]
# v[218] = [218, "afkjdl;s"]
# v[179] = [179, "klj;we"]

# printGrid(v)

# print(calcTotalMH(v, {28, 29}, {1, 2}))