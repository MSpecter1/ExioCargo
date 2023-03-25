class newGrid:
    def __init__(self, grid, depth, offContainers, loadContainers, isGrabbing, parentNode, action, offloadedContainers):
        self.grid = grid
        self.depth = depth
        self.offContainers = offContainers
        self.loadContainers = loadContainers
        self.isGrabbing = isGrabbing
        self.parentNode = parentNode
        self.action = action
        self.offloadedContainers = offloadedContainers

    def getGrid(self):
        return self.grid

    def getDepth(self):
        return self.depth

    def getOffContainers(self):
        return self.offContainers

    def getLoadContainers(self):
        return self.loadContainers

    def getIsGrabbing(self):
        return self.isGrabbing

    def setParentNode(self, node):
        self.parentNode = node

    def getParentNode(self):
        return self.parentNode
    
    def getAction(self):
        return self.action
    
    def getOffloadedContainers(self):
        return self.offloadedContainers

    def calcHash(self):
        ret = 0
        for cell in range(390):
            if self.grid[cell][1] == "CRANE":
                ret += (cell * 10000000000000)
            elif self.grid[cell][1] != "UNUSED" and self.grid[cell][1] != "TRUCK" and self.grid[cell][1] != "NAN":
                ret += (cell * 70)
        for i in range(len(self.offContainers)):
            ret += 1000000
        for i in range(len(self.loadContainers)):
            ret += 1000
        if self.isGrabbing:
            ret += 1
        return ret