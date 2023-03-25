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
            # print("up")
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = "UNUSED"
            newGrid[cranePos + 39][1] = "CRANE"
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "up", newOffloadedContainers))
        if(cranePos >= 66):        #CRANE_MOVEDOWN
            if(grid[cranePos - 39][1] == "UNUSED"):
                # print("down")
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "CRANE"
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "down", newOffloadedContainers))
        if((cranePos % 39 != 0) and (grid[cranePos - 1][1] == "UNUSED")):       #CRANE_MOVELEFT
            # print("left")
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = "UNUSED"
            newGrid[cranePos - 1][1] = "CRANE"
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "left", newOffloadedContainers))
        if(((cranePos - 38) % 39 != 0)):       #CRANE_MOVERIGHT
            if(grid[cranePos + 1][1] == "UNUSED"):
                # print("right")
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos + 1][1] = "CRANE"
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "right", newOffloadedContainers))
        if(cranePos == 376):
            if(createGrid.newGrid.getLoadContainers(self)):
                # print("grab")
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                container = newLoadContainers[0]
                newIsGrabbing = container
                newLoadContainers.remove(container)
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "grab", newOffloadedContainers))
        elif((grid[cranePos - 39][1] != "UNUSED") and (grid[cranePos - 39][1] != "TRUCK") and (grid[cranePos - 39][1] != "NAN")):       #CRANE_GRAB
            # print("grab")
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newIsGrabbing = grid[cranePos - 39][1]
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "grab", newOffloadedContainers))
        return ret
    else:
        if(cranePos <= 350):        #CRANE_MOVEUP
            # print("up")
            newGrid = copy.deepcopy(grid)
            newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
            newDepth += 1
            newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
            newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
            newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
            newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
            newGrid[cranePos][1] = currentlyGrabbing
            newGrid[cranePos + 39][1] = "CRANE"
            newGrid[cranePos - 39][1] = "UNUSED"
            ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "up", newOffloadedContainers))
        if(cranePos >= 105):     #CRANE_MOVEDOWN
            if(grid[cranePos - 78][1] == "UNUSED"):
                # print("down")
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "CRANE"
                newGrid[cranePos - 78][1] = currentlyGrabbing
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "down", newOffloadedContainers))
        if((cranePos % 39 != 0)):
            if((grid[cranePos - 1][1] == "UNUSED") and (grid[cranePos - 39 - 1][1] == "UNUSED")):       #CRANE_MOVELEFT
                # print("left")
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "UNUSED"
                newGrid[cranePos - 1][1] = "CRANE"
                newGrid[cranePos - 39 - 1][1] = currentlyGrabbing
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "left", newOffloadedContainers))
        if((cranePos - 38) % 39 != 0):      #CRANE_MOVERIGHT
            if((grid[cranePos + 1][1] == "UNUSED") and (grid[cranePos - 39 + 1][1] == "UNUSED")):
                # print("right")
                newGrid = copy.deepcopy(grid)
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newGrid[cranePos][1] = "UNUSED"
                newGrid[cranePos - 39][1] = "UNUSED"
                newGrid[cranePos + 1][1] = "CRANE"
                newGrid[cranePos - 39 + 1][1] = currentlyGrabbing
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "right", newOffloadedContainers))
        if(cranePos == 376):        #CRANE_RELEASE (if crane is above truck)
            if(currentlyGrabbing in createGrid.newGrid.getOffContainers(self)):
                # print("release-- crane/container is currently above truck")
                newGrid = copy.deepcopy(grid)
                newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                newOffloadedContainers.append(currentlyGrabbing)
                newGrid[337][1] = "UNUSED"
                newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                newDepth += 1
                newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                newOffContainers.remove(currentlyGrabbing)
                newIsGrabbing = ""
                ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "release", newOffloadedContainers))
        elif(cranePos <= 350):
            if(grid[cranePos - 78][1] != "UNUSED"):     #CRANE_RELEASE (for all other (valid) scenarios)
                if(((cranePos - 24) % 39 != 0) and ((cranePos - 26) % 39 != 0)):
                    # print("release")
                    newGrid = copy.deepcopy(grid)
                    newDepth = copy.deepcopy(createGrid.newGrid.getDepth(self))
                    newDepth += 1
                    newOffloadedContainers = copy.deepcopy(createGrid.newGrid.getOffloadedContainers(self))
                    newOffloadedContainers.append(currentlyGrabbing)
                    newOffContainers = copy.deepcopy(createGrid.newGrid.getOffContainers(self))
                    newLoadContainers = copy.deepcopy(createGrid.newGrid.getLoadContainers(self))
                    newIsGrabbing = copy.deepcopy(createGrid.newGrid.getIsGrabbing(self))
                    newIsGrabbing = ""
                    ret.append(createGrid.newGrid(newGrid, newDepth, newOffContainers, newLoadContainers, newIsGrabbing, None, "release", newOffloadedContainers))
        return ret
