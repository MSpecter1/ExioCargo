class newGrid:
    def __init__(self, grid, depth, offContainers, loadContainers, isGrabbing):
        self.grid = grid
        self.depth = depth
        self.offContainers = offContainers
        self.loadContainers = loadContainers
        self.isGrabbing = isGrabbing

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