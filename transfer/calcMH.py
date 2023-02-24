import copy

def calcTotalMH(grid, offContainers, loadContainers):    #'grid' refers to the current grid. 'offContainers' refers to the containers that need to be offloaded
    cost = 0

    for cell in range(351):
        if grid[cell][1] in offContainers:
            cost += calcDistanceFromTruck(cell)
            aboveLoc = copy.deepcopy(cell)
            aboveLoc += 39
            while(aboveLoc <= 311):
                if (grid[aboveLoc][1] != "UNUSED") and not(grid[aboveLoc][1] in offContainers):
                    cost += 100
                    # TODO: calculate the nearest cell that the containers can go
                aboveLoc += 39

            # print("cost for v[", cell, "] is: ", cost)

    for container in loadContainers:
        cost += 2 #"placeholder" cost value for containers that need to be loaded

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