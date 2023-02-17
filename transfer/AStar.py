from queue import PriorityQueue

from basicgrid import createBasic
from printgrid import printGrid
from calcMH import calcTotalMH
from modifyGrid import modifyGrid

v = createBasic()
v = modifyGrid(v)

# print(calcTotalMH(v, {27, 300, 38}))

# def AStarMH():
#     v = createBasic()
#     pq = PriorityQueue()