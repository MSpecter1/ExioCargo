import copy

def newCalcTotalMH(grid, offContainers, loadContainers, isGrabbing):
    # need to account for: all offloads, all containers above offloads, all loads, all buffers, if crane is grabbing

    cost = 0
    cranePos = findCrane(grid)

    for cell in range(351):
        if grid[cell][1] in offContainers:  #adding cost for offloads and all containers above offloads
            cost += distanceToTruck(cell)
            # print("offContainer cost: ", distanceToTruck(cell))
            aboveLoc = copy.deepcopy(cell)
            aboveLoc += 39
            while(aboveLoc <= 311):
                if(grid[aboveLoc][1] != "UNUSED" and grid[aboveLoc][1] != "CRANE" and not(grid[aboveLoc][1] in offContainers)):
                    cost += calcNearestValidSpot(grid, offContainers, aboveLoc, isGrabbing)
                    # print("cost for container above offload: ", calcNearestValidSpot(grid, offContainers, aboveLoc, isGrabbing))
                aboveLoc += 39
        if((cell >= 156 and cell <= 179) or (cell >= 195 and cell <= 218) or (cell >= 234 and cell <= 257) or (cell >= 273 and cell <= 296)) and (grid[cell][1] != "UNUSED" and grid[cell][1] != "NAN" and grid[cell][1] != "CRANE") and not(isGrabbing):
            bufferCell = copy.deepcopy(cell)
            if(distanceToShip(grid, offContainers, bufferCell) != -1):
                cost += distanceToShip(grid, offContainers, bufferCell)
                # print("bufferCell cost: ", distanceToShip(grid, offContainers, bufferCell))
    
    for i in range(len(loadContainers)):
        cost += calcNearestValidSpot(grid, offContainers, 337, isGrabbing)

    if(isGrabbing):
        container = cranePos - 39
        if(grid[container][1] not in offContainers):
            cost += calcNearestValidSpot(grid, offContainers, container, isGrabbing)
            # print("isGrabbing cost: ", calcNearestValidSpot(grid, offContainers, container, isGrabbing))
    else:
        nearestAction = []
        for cell in range(312):
            if grid[cell][1] in offContainers:
                aboveLoc = copy.deepcopy(cell)
                aboveLoc += 39
                while(grid[aboveLoc][1] != "UNUSED" and grid[aboveLoc][1] != "CRANE"):
                    aboveLoc += 39
                nearestAction.append(distanceToCell(cranePos, aboveLoc))
            if((cell >= 156 and cell <= 179) or (cell >= 195 and cell <= 218) or (cell >= 234 and cell <= 257) or (cell >= 273 and cell <= 296)) and (grid[cell][1] != "UNUSED" and grid[cell][1] != "NAN" and grid[cell][1] != "CRANE") and not(isGrabbing):
                if(distanceToShip(grid, offContainers, cell) != -1):
                    nearestAction.append(distanceToBuffer(grid, cranePos, isGrabbing))
        if(loadContainers):
            nearestAction.append(distanceToTruck(cranePos))
        if(nearestAction):
            cost += min(nearestAction)
            # print("nearestAction cost: ", min(nearestAction))
    
    return cost


def calcNearestValidSpot(grid, offContainers, cell, isGrabbing):
    toShip = distanceToShip(grid, offContainers, cell)
    if(toShip != -1):
        return toShip
    else:
        return distanceToBuffer(grid, cell, isGrabbing)

def distanceToTruck(cell):
    rows = cell // 39
    col = abs(cell - (rows * 39))
    rows = 8 - rows
    cols = abs(col - 25)
    return (rows + cols)

def distanceToShip(grid, offContainers, startCell):
    nearest = []
    for i in range(12):
        cell = 27 + i
        offContainerInColumn = False
        colCell = copy.deepcopy(cell)
        while(grid[colCell][1] != "UNUSED" and grid[colCell][1] != "CRANE"):
            if grid[colCell][1] in offContainers:
                offContainerInColumn = True
            colCell += 39
        if(colCell <= 311 and not offContainerInColumn):
            nearest.append(distanceToCell(startCell, colCell))
    if nearest:
        return min(nearest)
    else:
        return -1

def distanceToBuffer(grid, startCell, isGrabbing):
    nearest = []
    for i in range(24):
        cell = 156 + i
        colCell = copy.deepcopy(cell)

        if(isGrabbing):
            while(grid[colCell][1] != "UNUSED" and grid[colCell][1] != "CRANE"):
                if(grid[colCell + 39][1] == "CRANE"):
                    if(colCell <= 296):
                        # nearest.append(distanceToCell(startCell, colCell))
                        return 0
                colCell += 39
            if(colCell <= 296):
                nearest.append(distanceToCell(startCell, colCell))
        else:
            while(grid[colCell][1] != "UNUSED" and grid[colCell][1] != "CRANE"):
                colCell += 39
            if(colCell <= 296):
                nearest.append(distanceToCell(startCell, colCell))
    return min(nearest)

def distanceToCell(start, end):
    row1 = start // 39
    row2 = end // 39
    rows = abs(row1 - row2)
    col1 = start - (row1 * 39)
    col2 = end - (row2 * 39)
    cols = abs(col1 - col2)
    return (rows + cols)

def findCrane(grid):
    for cell in range(390):
        if grid[cell][1] == "CRANE":
            return cell