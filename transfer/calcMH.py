import math

def calcTotalMH(grid, offContainers):    #'grid' refers to the current grid. 'offContainers' refers to the containers that need to be offloaded
    cost = 0
    for container in offContainers:
        cost += calcMHOffload(calcConvertedCellOffload(container))
    return cost
    # need to calculate (and add onto total) the manhattan distance for all containers in buffer

def calcConvertedCellOffload(pos: int):
    if pos <= 38:
        x = 1
    elif pos <= 77:
        x = 2
    elif pos <= 116:
        x = 3
    elif pos <= 155:
        x = 4
    elif pos <= 194:
        x = 5
    elif pos <= 233:
        x = 6
    elif pos <= 272:
        x = 7
    elif pos <= 311:
        x = 8
    x = x * 27
    return (pos - x)

def calcMHOffload(convertedCell):
    rows = math.ceil((96 - convertedCell) / 12)
    cols = convertedCell % 12 + 2
    # print("Container at cell ", convertedCell, " needs to move ", rows, " rows up, and ", cols, " columns left.")
    return rows + cols