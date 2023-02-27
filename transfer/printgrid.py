# class printGrid:
    
def printGrid(vec):
    for row in range(9, -1, -1):
        for i in range(39):
            if vec[(row * 39) + i][1] == "NAN":
                print(chr(0x2588), end = " ")
            elif vec[(row * 39) + i][1] == "BUFFER":
                print("B", end = " ")
            elif vec[(row * 39) + i][1] == "TRUCK":
                print("T", end = " ")
            elif vec[(row * 39) + i][1] == "UNUSED":
                print("_", end = " ")
            elif vec[(row * 39) + i][1] == "CRANE":
                print("H", end = " ")
            else:
                print("C", end = " ")   #container
        print()




    # for i in range(39):
    #     # if vec[i][1] == "NAN":
    #     #     print(i, chr(0x2588), end="   ")
    #     # elif vec[i][1] == "SHIP":
    #     #     print(i, 'S', end="   ")
    #     # else:
    #     #     print(i, "ERROR", end="   ")

    #     if vec[i][1] == "NAN":
    #         print(chr(0x2588), end=" ")
    #     elif vec[i][1] == "SHIP":
    #         print("S", end=" ")
    #     elif vec[i][1] == ""
    #     else:
    #         print("ERROR", end=" ")