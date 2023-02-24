from queue import PriorityQueue
import copy

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
offContainers = ["Doe"]
loadContainers = ["Nat"]
start = createGrid.newGrid(v, 0, offContainers, loadContainers, "")

print("INITIAL STATE:")
printGrid(createGrid.newGrid.getGrid(start))
print("Initial MH is: ", calcTotalMH(start.getGrid(), offContainers, loadContainers))

finished = False

solution = any

pq = PriorityQueue()
pq.put(PriorityEntry((start.getDepth() + calcTotalMH(start.getGrid(), offContainers, loadContainers)), start))

# mh = start.getDepth() + calcTotalMH(start.getGrid(), offContainers, loadContainers)
hmap = {}
hmap[createGrid.newGrid.calcHash(start)] = None

while pq:
    node = pq.get()
    # print(type(node))
    curr = node.getData()
    # print(node.getData())
    if isGoalState(createGrid.newGrid.getGrid(curr), createGrid.newGrid.getOffContainers(curr), createGrid.newGrid.getLoadContainers(curr), createGrid.newGrid.getIsGrabbing(curr)):
        solution = node
        break
    nodes = expandMoves.expandMoves(curr)
    for n in nodes:
        # pq.put((n.getDepth() + calcTotalMH(n.getGrid(), n.getOffContainers(), n.getLoadContainers)), n)
        tempMH = createGrid.newGrid.getDepth(n) + calcTotalMH(createGrid.newGrid.getGrid(n), createGrid.newGrid.getOffContainers(n), createGrid.newGrid.getLoadContainers(n))
        hash = createGrid.newGrid.calcHash(n)
        if hash not in hmap:
            hmap[hash] = None
            pq.put(PriorityEntry(tempMH, n))
            # if mh != tempMH:
            #     mh = tempMH
            print("\nPutting the following grid with MH of ", tempMH, " into PQ:")
            printGrid(createGrid.newGrid.getGrid(n))

#priorityentry BS taken from https://stackoverflow.com/questions/40205223/priority-queue-with-tuples-and-dicts

if(solution):
    print("Solution found")
else:
    print("No solution found :(")


# v[178] = [178, "asdklf"]
# v[218] = [218, "afkjdl;s"]
# v[179] = [179, "klj;we"]

# printGrid(v)

# print(calcTotalMH(v, {28, 29}, {1, 2}))