from queue import PriorityQueue

from basicgrid import createBasic
from printgrid import printGrid
from calcMH import calcTotalMH

v = createBasic()
print(calcTotalMH(v, {27, 300, 38}))

# def AStarMH():
#     v = createBasic()
#     pq = PriorityQueue()