def isGoalState(grid, offContainers, loadContainers, isGrabbing):
    ret = True
    for i in range(24):
        if grid[156 + i][1] != "UNUSED":
            ret = ret and False
        if grid[195 + i][1] != "UNUSED":
            ret = ret and False
        if grid[234 + i][1] != "UNUSED":
            ret = ret and False
        if grid[273 + i][1] != "UNUSED":
            ret = ret and False
    
    if offContainers:
        ret = ret and False
    if loadContainers:
        ret = ret and False

    if isGrabbing:
        ret = ret and False
    
    return ret