import createGrid
import copy

def expandMoves(self):
    ret = []
    grid = createGrid.newGrid.getGrid(self)
    currentlyGrabbing = createGrid.newGrid.getIsGrabbing(self)
    for cell in range(390):
        if grid[cell][1] == "CRANE":
            cranePos = cell

    if(not(currentlyGrabbing)):
        if(cranePos <= 350):    #CRANE_MOVEUP
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = "UNUSED"
            newGrid[cranePos + 39][1] = "CRANE"
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if(cranePos >= 66):        #CRANE_MOVEDOWN
            if(grid[cranePos - 39][1] == "UNUSED"):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "CRANE"
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if((cranePos % 39 != 0) and (grid[cranePos - 1][1] == "UNUSED")):       #CRANE_MOVELEFT
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = "UNUSED"
            newGrid[cranePos - 1][1] = "CRANE"
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if(((cranePos - 38) % 39 != 0)):       #CRANE_MOVERIGHT
            if(grid[cranePos + 1][1] == "UNUSED"):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos + 1][1] = "CRANE"
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if(cranePos == 376):
            if(not(createGrid.newGrid.getLoadContainers(self))):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                container = newLoadContainers[0]
                newIsGrabbing = container
                newLoadContainers.remove(container)
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        elif(grid[cranePos - 39][1] != ("UNUSED" or "TRUCK" or "NAN")):       #CRANE_GRAB
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newIsGrabbing = grid[cranePos - 39][1]
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        return ret
    else:
        if(cranePos <= 350):        #CRANE_MOVEUP
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = currentlyGrabbing
            newGrid[cranePos + 39][1] = "CRANE"
            newGrid[cranePos - 39][1] = "UNUSED"
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if(cranePos >= 105):     #CRANE_MOVEDOWN
            if(grid[cranePos - 78][1] == "UNUSED"):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "CRANE"
                newGrid[cranePos - 78][1] = currentlyGrabbing
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if((cranePos % 39 != 0) and (grid[cranePos - 1][1] == "UNUSED") and (grid[cranePos - 39 - 1] == "UNUSED")):     #CRANE_MOVELEFT
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = "UNUSED"
            newGrid[cranePos - 39][1] = "UNUSED"
            newGrid[cranePos - 1][1] = "CRANE"
            newGrid[cranePos - 39 - 1][1] = currentlyGrabbing
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if((cranePos - 38) % 39 != 0):      #CRANE_MOVERIGHT
            if((grid[cranePos + 1][1] == "UNUSED") and (grid[cranePos - 39 + 1][1] == "UNUSED")):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "UNUSED"
                newGrid[cranePos + 1][1] = "CRANE"
                newGrid[cranePos - 39 + 1][1] = currentlyGrabbing
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        if(cranePos == 376):        #CRANE_RELEASE (if crane is above truck)
            if(currentlyGrabbing in createGrid.newGrid.getOffContainers(self)):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newOffContainers.remove(currentlyGrabbing)
                newIsGrabbing = ""
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        elif(grid[cranePos - 78][1] != "UNUSED"):       #CRANE_RELEASE (for all other (valid) scenarios)
            if(((cranePos - 24) % 39 != 0) and ((cranePos - 26) % 39 != 0)):
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newIsGrabbing = ""
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing))
        return ret
