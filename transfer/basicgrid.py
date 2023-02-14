import numpy as np

from printgrid import printGrid

v = []

for x in range(4):
    for n in range(27):
        list = [(x * 39) + n, "NAN"]
        v.append(list)
    for s in range(12):
        list = [(x * 39) + 27 + s, "SHIP"]
        v.append(list)

for x in range(3):
    for b in range(24):
        list = [156 + (x * 39) + b, "BUFFER"]
        v.append(list)
    for n in range(3):
        list = [156 + (x * 39) + 24 + n, "NAN"]
        v.append(list)
    for s in range(12):
        list = [156 + (x * 39) + 27 + s, "SHIP"]
        v.append(list)

for b in range(24):
    list = [273 + b, "BUFFER"]
    v.append(list)

v.append([297, "NAN"])
v.append([298, "TRUCK"])
v.append([299, "NAN"])

for s in range(12):
    list = [300 + s, "SHIP"]
    v.append(list)

for u in range(39):
    list = [312 + u, "UNUSED"]
    v.append(list)

# print(v)
printGrid(v)