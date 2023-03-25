import copy

def calcTotalMH(grid, offContainers, loadContainers, isGrabbing):    #'grid' refers to the current grid. 'offContainers' refers to the containers that need to be offloaded
    cost = 0

    # TODO (might need to): calculate the MH for the container the crane is currently grabbing
    if(isGrabbing):
        for cell in range(390):
            if grid[cell][1] == "CRANE":
                cranePos = cell
        grabbedContainer = cranePos - 39
        if(grid[grabbedContainer][1] not in offContainers):
            cost += calcLowestCost(grid, offContainers, grabbedContainer)
            # print("calculating MH for isGrabbing: ", calcLowestCost(grid, offContainers, grabbedContainer))
            # currently the algorithm repeats the cost for the container the crane is grabbing
    else:
        # print("crane is not grabbing")
        nearest = []
        for cell in range(390):
            if grid[cell][1] == "CRANE":
                cranePos = cell
        for cell in range(351):
            if grid[cell][1] in offContainers:
                aboveLoc = copy.deepcopy(cell)
                aboveLoc += 39
                while(grid[aboveLoc][1] != "UNUSED" and grid[aboveLoc][1] != "CRANE"):
                    aboveLoc += 39
                nearest.append(calcDistanceFromCell(cranePos, aboveLoc))
                # print("cost for crane to top of column: ", calcDistanceFromCell(cranePos, aboveLoc))
        if(loadContainers):
            nearest.append(calcDistanceFromTruck(cranePos))
        if(nearest):
            cost += min(nearest)

    for cell in range(351):     #DOESN'T WORK FOR OFFLOAD CONTAINERS IN BUFFER YET
        if grid[cell][1] in offContainers:
            cost += calcDistanceFromTruck(cell)
            # print("+", calcDistanceFromTruck(cell), " from calcDistanceFromTruck")
            aboveLoc = copy.deepcopy(cell)
            aboveLoc += 39
            while(aboveLoc <= 311):     #MIGHT NEED TO WORK ON THIS (currently repeats cost for containers that were already counted)
                if(grid[aboveLoc][1] != "UNUSED" and grid[aboveLoc][1] != "CRANE" and not(grid[aboveLoc][1] in offContainers)):
                    cost += calcLowestCost(grid, offContainers, aboveLoc)
                aboveLoc += 39

            # print("cost for v[", cell, "] is: ", cost)

    # for container in loadContainers:
    #     cost += 2 #"placeholder" cost value for containers that need to be loaded
    
    for i in range(len(loadContainers)):
        cost += calcLowestCost(grid, offContainers, 337)

    for i in range(24):
        if grid[156 + i][1] != "UNUSED" and not(grid[156 + i][1] in offContainers) and grid[156 + i][1] != "CRANE":
            cost += calcLowestCost(grid, offContainers, (156 + i))
        if grid[195 + i][1] != "UNUSED" and not(grid[195 + i][1] in offContainers) and grid[195 + i][1] != "CRANE":
            cost += calcLowestCost(grid, offContainers, (195 + i))
        if grid[234 + i][1] != "UNUSED" and not(grid[234 + i][1] in offContainers) and grid[234 + i][1] != "CRANE":
            cost += calcLowestCost(grid, offContainers, (234 + i))
        if grid[273 + i][1] != "UNUSED" and not(grid[273 + i][1] in offContainers) and grid[273 + i][1] != "CRANE":
            cost += calcLowestCost(grid, offContainers, (273 + i))
    return cost

def calcLowestCost(grid, offContainers, cell):
    cost = []
    # for i in range(24):
    #     x = 156 + i
    #     while(grid[x][1] != "UNUSED" and grid[x][1] != "CRANE"):
    #         x += 39
    #     if(x <= 296):
    #         cost.append(calcDistanceFromCell(cell, x))
    for i in range(12):
        offContainerInColumn = False
        x = 27 + i
        while(grid[x][1] != "UNUSED" and grid[x][1] != "CRANE"):
            if(grid[x][1] in offContainers):
                offContainerInColumn = True
            x += 39
        if(x <= 311 and not(offContainerInColumn)):
            cost.append(calcDistanceFromCell(cell, x))
    if(cost):
        return min(cost)
    else:
        # return 40
        return calcCostToBuffer(grid, cell)
    # return min(cost)

def calcCostToBuffer(grid, cell):
    cost = []
    for i in range(24):
        x = 156 + i
        while(grid[x][1] != "UNUSED" and grid[x][1] != "CRANE"):
            x += 39
        if(x <= 296):
            cost.append(calcDistanceFromCell(cell, x))
    return min(cost)

def calcDistanceFromTruck(cell):
    rows = cell // 39
    col = cell - (rows * 39)
    rows = 8 - rows
    cols = abs(col - 25)
    return (rows + cols)

def calcDistanceFromCell(start, end):
    row1 = start // 39
    row2 = end // 39
    rows = abs(row1 - row2)
    col1 = start - (row1 * 39)
    col2 = end - (row2 * 39)
    cols = abs(col1 - col2)
    return (rows + cols)