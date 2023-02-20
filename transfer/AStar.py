from queue import PriorityQueue
import copy

from basicgrid import createBasic
from printgrid import printGrid
from calcMH import calcTotalMH
from modifyGrid import modifyGrid
from goalState import isGoalState
import createGrid

v = createBasic()
v = modifyGrid(v)
offContainers = []
loadContainers = []
start = createGrid.newGrid(v, 0, offContainers, loadContainers, "")

finished = False

solution = any

pq = PriorityQueue()
pq.put((start.getDepth() + calcTotalMH(start.getGrid()), start))

while pq:
    node = pq.get()
    if isGoalState(node[1], createGrid.newGrid.getOffContainers(node[1]), createGrid.newGrid.getLoadContainers(node[1]), createGrid.newGrid.getIsGrabbing(node[1])):
        solution = node
        break
    nodes = expand()

if(solution):
    print("Solution found")
else:
    print("No solution found :(")




# v[178] = [178, "asdklf"]
# v[218] = [218, "afkjdl;s"]
# v[179] = [179, "klj;we"]

# printGrid(v)

# print(calcTotalMH(v, {28, 29}, {1, 2}))