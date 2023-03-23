import Balance

# To test, install pytest using "pip install pytest", then enter "pytest" to run through all tests (including the edge case tests)
def test_ShipCase1():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\ShipCase1.txt")
    if result and result.crane_movement_cells  == 13:
        assert True
    else:
        assert False

def test_ShipCase2():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\ShipCase2.txt")
    if result and result.crane_movement_cells  == 20:
        assert True
    else:
        assert False

def test_ShipCase3():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\ShipCase3.txt")
    if result and result.crane_movement_cells  == 23:
        assert True
    else:
        assert False

def test_ShipCase4():   
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\ShipCase4.txt")
    if result and result.crane_movement_cells  == 41:
        assert True
    else:
        assert False

def test_ShipCase5():
    test_search = Balance.CargoSearch()
    test_state = Balance.ShipState()
    result = test_search.search(test_state, "Balance\TestManifests\ShipCase5.txt")
    if result and result.crane_movement_cells  == 40:
        assert True
    else:
        assert False