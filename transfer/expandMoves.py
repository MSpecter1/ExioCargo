import createGrid
import copy

def expandMoves(self):
    ret = []
    grid = createGrid.newGrid.getGrid(self)
    for cell in grid:
        if grid[cell][1] == "CRANE":
            cranePos = grid[cell][0]
    if(cranePos) <= 389:    #CRANE_MOVEUP
        newGrid = copy.deepcopy(grid)
        newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
        newDepth += 1
        newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
        newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
        newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
        newGrid[cranePos] = [cranePos, "UNUSED"]
        newGrid[cranePos + 39][1] = "CRANE"
        ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
    if(grid[cranePos - 39] == "UNUSED"):    #CRANE_MOVEDOWN
        newGrid = copy.deepcopy(grid)
        newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
        newDepth += 1
        newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
        newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
        newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
        newGrid[cranePos][1] = "UNUSED"
        newGrid[cranePos - 39][1] = "CRANE"
        ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
    if((cranePos % 39 != 0) and (grid[cranePos - 39 - 1] == "UNUSED")):
        newGrid = copy.deepcopy(grid)
        newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
        newDepth += 1
        newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
        newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
        newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
        newGrid[cranePos][1] = "UNUSED"
        # newGrid[cranePos - 39] not finished lol
        #TODO: check over the cranePos and make sure it's the right ones