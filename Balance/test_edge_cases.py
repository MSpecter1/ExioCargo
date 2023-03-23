import Balance

# No containers
def test_EdgeCase1():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase1.txt")
    if result and result.crane_movement_cells  == 0:
        assert True
    else:
        assert False
# One container, impossible to balance so expect SIFT
def test_EdgeCase2():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase2.txt")
    if result and result.crane_movement_cells  == 12:
        assert True
    else:
        assert False

# Balance where one container needs to be moved
def test_EdgeCase3():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase3.txt")
    if result and result.crane_movement_cells  == 13:
        assert True
    else:
        assert False

# Balance where one container needs to be moved, but its stacked on top of another container
def test_EdgeCase4():   
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase4.txt")
    if result and result.crane_movement_cells  == 13:
        assert True
    else:
        assert False

# Balance where two containers need to move
def test_EdgeCase5():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase5.txt")
    if result and result.crane_movement_cells  == 20:
        assert True
    else:
        assert False

# Balance where one container is named "NAN" and needs to be moved
def test_EdgeCase6():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase6.txt")
    if result and result.crane_movement_cells  == 13:
        assert True
    else:
        assert False

# Balance ship is full and already balanced
def test_EdgeCase7():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase7.txt")
    if result and result.crane_movement_cells  == 0:
        assert True
    else:
        assert False

# Balance ship is almost full and needs to move one container to balance
def test_EdgeCase8():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase8.txt")
    if result and result.crane_movement_cells  == 12:
        assert True
    else:
        assert False

# Ship container area with only one row (everything else is nan), same solution as previous
def test_EdgeCase9():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase9.txt")
    if result and result.crane_movement_cells  == 12:
        assert True
    else:
        assert False

# Ship container area only has two columns
def test_EdgeCase10():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase10.txt")
    if result and result.crane_movement_cells  == 12:
        assert True
    else:
        assert False

# Move one container over big column of containers
def test_EdgeCase11():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase11.txt")
    if result and result.crane_movement_cells  == 29:
        assert True
    else:
        assert False

# SIFT where all containers are on the same row, need to stack one container temporarily
def test_EdgeCase12():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase12.txt")
    if result and result.crane_movement_cells  == 30:
        assert True
    else:
        assert False

# SIFT no movement needed
def test_EdgeCase13():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase13.txt")
    if result and result.crane_movement_cells  == 0:
        assert True
    else:
        assert False
        
# SIFT move one container
def test_EdgeCase14():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase14.txt")
    if result and result.crane_movement_cells  == 12:
        assert True
    else:
        assert False

# SIFT move two containers
def test_EdgeCase15():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\EdgeCase15.txt")
    if result and result.crane_movement_cells  == 21:
        assert True
    else:
        assert False

def generateFULL():
    name = "TEST"
    cnt = 0
    f = open("FULL_MANIFEST"+"OUTPUT.txt", "w")
    for j in range(8):
        for i in range(12):
            cnt+=1
            f.write('['+str("%02d"%(j+1))+','+str("%02d"%(i+1))+'], {'+str("%05d"%100)+'}, '+str(name+str(cnt))+'\n')

def generateNAN():
    name = "TEST"
    cnt = 0
    f = open("NAN_MANIFEST"+"OUTPUT.txt", "w")
    for j in range(8):
        for i in range(12):
            cnt+=1
            if False: #i in range(0,5) or i in range(7,12)
                f.write('['+str("%02d"%(j+1))+','+str("%02d"%(i+1))+'], {'+str("%05d"%0)+'}, '+str('NAN')+'\n')
            elif i == 5:
                f.write('['+str("%02d"%(j+1))+','+str("%02d"%(i+1))+'], {'+str("%05d"%100)+'}, '+str(name+str(cnt))+'\n')
            else:
                f.write('['+str("%02d"%(j+1))+','+str("%02d"%(i+1))+'], {'+str("%05d"%0)+'}, '+str('UNUSED')+'\n')

# generateNAN()