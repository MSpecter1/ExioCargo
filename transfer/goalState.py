def isGoalState(grid, offContainers, loadContainers, isGrabbing):
    ret = True
    for i in range(24):
        if grid[156 + i][1] != "UNUSED" and grid[156 + i][1] != "NAN":
            ret = False
        if grid[195 + i][1] != "UNUSED" and grid[195 + i][1] != "NAN":
            ret = False
        if grid[234 + i][1] != "UNUSED" and grid[234 + i][1] != "NAN":
            ret = False
        if grid[273 + i][1] != "UNUSED" and grid[273 + i][1] != "NAN":
            ret = False
    
    if offContainers:
        ret = False
    if loadContainers:
        ret = False

    if isGrabbing:
        ret = False
    
    return ret