import numpy as np
import ManifestReader
from queue import PriorityQueue

class ShipState:
    balanced = None
    balance_key = None

    def __init__(self):
        self.state = np.empty((8,12), dtype=ManifestReader.container)
        self.numContainers = 0

    def load_state(self, manifest_link):
        test = ManifestReader.manifest_reader()
        test.set_manifest(manifest_link)
        containers = test.read_manifest()
        for c in containers:
            self.state[c.x][c.y] = c
            if c.name != 'NAN' and c.name != 'UNUSED':
                self.numContainers+=1

    def print_state(self):
        for s in np.flipud(self.state): # flip array up down so that "0,0" is displayed in the bottom left corner 
            getName = np.vectorize(ManifestReader.container.getName)
            print(getName(s))

class BalanceOperations:
    def checkBalance(self, ship_state):
        leftSum = 0
        rightSum = 0
        for row in ship_state.state:
            for container in row:
                if container.y<=5:
                    leftSum += container.weight
                else:
                    rightSum += container.weight
        # print(leftSum,",", rightSum)
        if leftSum == 0 and rightSum == 0:
            ship_state.balance = True
        elif ship_state.numContainers == 1:
            ship_state.balance = True
        elif rightSum <= leftSum*1.1 and rightSum >= leftSum*0.9:
            ship_state.balance = True
        else:
            ship_state.balance = False
        
        if leftSum == 0:
            ship_state.balance_key = 0
        elif rightSum == 0:
            ship_state.balance_key = 0
        else:
            k1 = leftSum/rightSum
            k2 = rightSum/leftSum
            ship_state.balance_key = min(k1,k2)
        

class AStarSearch:
    frontier = PriorityQueue()
    explored = [] # np.isin(obj, explored)

    bop = BalanceOperations()

    def search(self, ship_state, manifest_link):
        ship_state.load_state(manifest_link)
        self.bop.checkBalance(ship_state)

        self.frontier.put(ship_state.balance_key, ship_state)

        while not self.frontier.empty():
            


test_state = ShipState()
test_state.load_state("Balance\ShipCase1.txt")
test_state.print_state()
print('Container Count: ',test_state.numContainers)

test_bop = BalanceOperations()
test_bop.checkBalance(test_state)
print('Balanced:', test_state.balanced)
print('Balance Key:', test_state.balance_key)