import copy

def calcTotalMH(grid, offContainers, loadContainers):    #'grid' refers to the current grid. 'offContainers' refers to the containers that need to be offloaded
    cost = 0

    # TODO (might need to): calculate the MH for the container the crane is currently grabbing

    for cell in range(351):     #DOESN'T WORK FOR OFFLOAD CONTAINERS IN BUFFER YET
        if grid[cell][1] in offContainers:
            cost += calcDistanceFromTruck(cell)
            # print("+", calcDistanceFromTruck(cell), " from calcDistanceFromTruck")
            aboveLoc = copy.deepcopy(cell)
            aboveLoc += 39
            while(aboveLoc <= 311):
                if (grid[aboveLoc][1] != "UNUSED") and not(grid[aboveLoc][1] in offContainers):
                    aboveCost = []
                    for i in range(12):
                        offContainerInColumn = False
                        start = aboveLoc
                        x = 27 + i
                        while(grid[x][1] != "UNUSED"):
                            if(grid[x][1] in offContainers):
                                offContainerInColumn = True
                            x += 39
                        if(x <= 311 and not(offContainerInColumn)):
                            aboveCost.append(calcDistanceFromCell(start, x))
                    cost += min(aboveCost)
                    # print("+", min(aboveCost), " from min(aboveCost)")
                aboveLoc += 39

            # print("cost for v[", cell, "] is: ", cost)

    # for container in loadContainers:
    #     cost += 2 #"placeholder" cost value for containers that need to be loaded
    
    i = len(loadContainers)
    cost += (2 * i)
    # print("+", (2 * i), " from loadContainers")

    for i in range(24):
        if grid[156 + i][1] != "UNUSED" and not(grid[156 + i][1] in offContainers) and grid[156 + i][1] != "CRANE":
            cost += 4 + (23 - i) + 4
        if grid[195 + i][1] != "UNUSED" and not(grid[195 + i][1] in offContainers) and grid[195 + i][1] != "CRANE":
            cost += 3 + (23 - i) + 4
        if grid[234 + i][1] != "UNUSED" and not(grid[234 + i][1] in offContainers) and grid[234 + i][1] != "CRANE":
            cost += 2 + (23 - i) + 4
        if grid[273 + i][1] != "UNUSED" and not(grid[273 + i][1] in offContainers) and grid[273 + i][1] != "CRANE":
            cost += 1 + (23 - i) + 4
    return cost

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