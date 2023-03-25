import numpy as np
import BalanceManifestReader
from queue import PriorityQueue
import copy
import time

import cProfile
from pstats import Stats

def manhattan(ch, cv, th, tv):
        return sum([abs(ch-th), abs(cv-tv)])

class ShipState:
    balanced = None
    balance_key = 0
    depth = 0

    crane_h = 0 # Crane's horizontal position, 0-7
    crane_v = 8 # Crane's vertical position, 0-11

    crane_movement_cells = 0
    holdsContainer = False # If crane is in position to lower and grab/move container, then this is true

    sizeH = 12
    sizeV = 9

    sift = False 
    filename = None

    state = None
    numContainers = None

    def __init__(self):
        self.state = np.empty((self.sizeV,self.sizeH), dtype=BalanceManifestReader.container)
        self.numContainers = 0
        self.solution = []

    def OutputManifest(self):
        f = open(self.filename+"OUTPUT.txt", "w")
        for j in range(8):
            for i in range(12):
                c = self.state[j][i]
                if c.name=='CRANE':
                    f.write('['+str("%02d"%(c.x+1))+','+str("%02d"%(c.y+1))+'], {'+str("%05d"%c.weight)+'}, '+str('UNUSED')+'\n')
                    continue
                f.write('['+str("%02d"%(c.x+1))+','+str("%02d"%(c.y+1))+'], {'+str("%05d"%c.weight)+'}, '+str(c.name)+'\n')

    def load_state(self, manifest_link):
        # Get Manifest
        test = BalanceManifestReader.manifest_reader()
        test.set_manifest(manifest_link)
        self.filename = manifest_link.split("\\")[-1].split(".")[0]
        self.containers = test.read_manifest()

        # Add containers to state
        for c in self.containers:
            self.state[c.x][c.y] = c #x is vertical, y is horizontal
        
        # Create Top Row for Crane
        for i in range(12):
            self.state[8][i] = BalanceManifestReader.container('UNUSED', 8 , i, 0, False, False)    
        self.state[8][0] = BalanceManifestReader.container('CRANE', 8,0,0, False, False)
        self.holdsContainer = False

    #  Print Array State and information, debug purposes
    def print_state(self):
        # Print state
        print('----------------------------------------------------------------------------------------------------')
        for s in np.flipud(self.state): # flip array up down so that "0,0" is displayed in the bottom left corner 
            getName = np.vectorize(BalanceManifestReader.container.getName)
            print(getName(s))
        print('----------------------------------------------------------------------------------------------------\n')

        print('Balanced:', self.balanced)
        print('Balance Key:', self.balance_key)
        print("Total Movement Cells:", self.crane_movement_cells)

        if not self.sift:
            print('heuristic', self.getHeuristic())
        else:
            print('heuristic SIFT', self.getHeuristicSift())

        print('Crane Moving To Hold Container?', self.holdsContainer)
        print('Crane Position:', self.crane_h, 'horizontal ',self.crane_v,' vertical')

        if self.solution:
            print('\nSolution Path:')
            for c in self.solution:
                print(c)
            print('\n')

    def increment_depth(self):
        self.depth += 1

    # Find heuristic for balance
    # Basis for deficit taken from professor Keogh's slides on search
    # https://www.dropbox.com/s/k0eo95kixkyln2p/Thoughts%20on%20N-column%20Container%20Search.pptx?dl=0
    def getHeuristic(self):
        #  Get list of all containers on each side and find the deficit
        left_sum = 0
        right_sum = 0
        right_c = []
        left_c = []
        for c in self.containers:
            if c.container and c.y<=5:
                left_sum += c.weight
                left_c.append(c)
            elif c.container and c.y>5:
                right_sum += c.weight
                right_c.append(c)

        total_sum = left_sum+right_sum
        if total_sum == 0:
            return 0
        score = min(left_sum,right_sum)/max(left_sum,right_sum) 
        if score>0.9:
            return 0

        right_c.sort(reverse=True)
        left_c.sort(reverse=True)

        target_mass = (left_sum+right_sum)/2
        left_deficit = target_mass-left_sum
        right_deficit = target_mass-right_sum
        
        # On the side with positive deficit (container needs to move to this side)
        # Get cost of moving container to the other side (underestimate since no crane movement/other containers on location taken into account) 
        if max(left_deficit, right_deficit) == left_deficit:
            h_cost = 0
            for c in right_c:
                if c.weight>=left_deficit*1.1:
                    continue
                if c.weight<=left_deficit*1.1:
                    left_deficit -= c.weight
                    h_cost += c.y - 5 
                    h_cost += c.x
                    # If there is a container above this container, it will require at least 1 unit movement horizontally and its vertical height to move it out of the way
                    if not c.x+1>8:
                        above_container = self.state[c.x+1][c.y]
                        if above_container.container:
                            h_cost += 1 + above_container.x 
            return h_cost

        elif max(left_deficit, right_deficit) == right_deficit:
            h_cost = 0
            for c in left_c:
                if c.weight>=right_deficit*1.1:
                    continue
                if c.weight<=right_deficit*1.1:
                    right_deficit -= c.weight
                    h_cost += 6 - c.y 
                    h_cost += c.x
                    # If there is a container above this container, it will require at least 1 unit movement horizontally and its vertical height to move it out of the way
                    if not c.x+1>8:
                        above_container = self.state[c.x+1][c.y]
                        if above_container.container:
                            h_cost += 1 + above_container.x 
            return h_cost

    # Get SIFT operation heuristic
    def getHeuristicSift(self):
        # Find the amount of containers possible in each row
        # each row can contain at most 12 containers unless there is 'NAN' 
        row_count = [12, 12, 12, 12, 12, 12, 12, 12] 
        for i in range(12):
            for j in range(8):
                if self.state[j][i].nan:
                    row_count[j] -= 1

        self.containers.sort(reverse=True)
        current_row = 0
        current_row_h_left = 5
        current_row_h_right = 6
        left = True
        h_cost = 0
        
        sum_cost = 0
        con_cnt = 0
        # move_list = []
        for c in self.containers:
            if c.container:
                con_cnt+=1
                total = 0
                if left:
                    total += abs(current_row_h_left - c.y)
                    target = self.state[current_row][current_row_h_left]
                    # if the target location has a container and its not the one that needs to be there
                    if target.container and target!=c:
                        total+=1
                    elif not target.container and not target.nan:
                        total+=1

                    # find if there is a need to move container over another one
                    heightNeeded = current_row
                    for c2 in self.containers:
                        if (c2.container or c2.nan) and c2.y in range(min(c.y, current_row_h_left),max(c.y, current_row_h_left)) and c2 != c:
                            if c2.x+1>heightNeeded:
                                heightNeeded = c2.x+1
                    if heightNeeded<current_row:
                        heightNeeded = current_row
                    total += abs(heightNeeded - c.x) + abs(current_row - heightNeeded)

                    current_row_h_left -= 1
                    left = False
                else:
                    total += abs(current_row_h_right - c.y)
                    target = self.state[current_row][current_row_h_right]
                    # if the target location has a container and its not the one that needs to be there
                    if target.container and target!=c:
                        total+=1
                    elif not target.container and not target.nan:
                        total+=1

                    # find if there is a need to move container over another one
                    heightNeeded = current_row
                    for c2 in self.containers:
                        if (c2.container or c2.nan) and c2.y in range(min(c.y, current_row_h_right),max(c.y, current_row_h_right)) and c2 != c:
                            if c2.x+1>heightNeeded:
                                heightNeeded = c2.x+1
                    if heightNeeded<current_row:
                        heightNeeded = current_row
                    total += abs(heightNeeded - c.x) + abs(current_row - heightNeeded)

                    current_row_h_right += 1
                    left = True

                sum_cost+= total

                row_count[current_row] -= 1
                if row_count[current_row] == 0:
                    current_row += 1
                    current_row_h_left = 6
                    current_row_h_right = 7
        h_cost+=sum_cost
        return(h_cost)
    
    def checkSift(self):
        # Find the amount of containers possible in each row
        # each row can contain at most 12 containers unless there is 'NAN' 
        row_count = [12, 12, 12, 12, 12, 12, 12, 12] 
        for i in range(12):
            for j in range(8):
                if self.state[j][i].nan:
                    row_count[j] -= 1

        self.containers.sort(reverse=True)
        current_row = 0
        current_row_h_left = 5
        current_row_h_right = 6
        left = True

        sum_cost = 0
        con_cnt = 0
        # move_list = []
        for c in self.containers:
            if c.container:
                con_cnt+=1
                total = 0
                local_overlap = 0
                if left:
            
                    total += abs(current_row_h_left - c.y)
                    total += abs(current_row - c.x)
                    current_row_h_left -= 1
                    left = False
                else:
                    total += abs(current_row_h_right - c.y)
                    total += abs(current_row - c.x)
                    current_row_h_right += 1
                    left = True
                sum_cost+= total

                row_count[current_row] -= 1
                if row_count[current_row] == 0:
                    current_row += 1
                    current_row_h_left = 6
                    current_row_h_right = 7
        if sum_cost ==0:
            return True
        return False

    def __lt__(self, other):
        if self.sift:
            return self.crane_movement_cells+self.getHeuristicSift() < other.crane_movement_cells+other.getHeuristicSift()
        else:            
            return self.crane_movement_cells+self.getHeuristic() < other.crane_movement_cells+other.getHeuristic()
    
    def __eq__(self, other):
        #  Equal if state is equal, also update movement cells if the same exact state is reached from different paths
        if (np.array_equal(self.state, other.state) and self.holdsContainer == other.holdsContainer):
            if self.crane_movement_cells<other.crane_movement_cells:
                other.crane_movement_cells = self.crane_movement_cells
            elif self.crane_movement_cells>other.crane_movement_cells:
                self.crane_movement_cells = other.crane_movement_cells 
            return True
        return False

class BalanceOperations:
    # Check if legally balanced and update balance score
    def checkBalance(self, ship_state):
        leftSum = 0
        rightSum = 0
        for row in ship_state.state:
            for container in row:
                if container.container and container.y<=5:
                    leftSum += container.weight
                elif container.container and container.y>5:
                    rightSum += container.weight

        if leftSum == 0 and rightSum == 0:
            ship_state.balanced = True
            ship_state.balance_key = 0
        else:
            # If Score == 1, it is perfectly balanced, so closer to 1 = closer to balance
            score = min(leftSum,rightSum)/max(leftSum,rightSum) 
            if score>0.9:
                ship_state.balanced = True
            else:
                ship_state.balanced = False
            ship_state.balance_key = score

    # Checks if it is impossible to balance
    def Possible(self, ship_state):
        left_sum = 0
        right_sum = 0
        right_c = []
        left_c = []
        for c in ship_state.containers:
            if c.container and c.y<=5:
                left_sum += c.weight
                left_c.append(c)
            elif c.container and c.y>5:
                right_sum += c.weight
                right_c.append(c)
        total_sum = left_sum+right_sum

        if total_sum == 0:
            return True
        score = min(left_sum,right_sum)/max(left_sum,right_sum) 
        if score>0.9:
            return True

        # Attempt potential moves to balance 
        right_c.sort(reverse=True)
        left_c.sort(reverse=True)

        target_mass = (left_sum+right_sum)/2
        left_deficit = target_mass-left_sum
        right_deficit = target_mass-right_sum

        h_cost = 0
        if max(left_deficit, right_deficit) == left_deficit:
            for c in right_c:
                if left_deficit<total_sum*0.1 and left_deficit>total_sum*-0.1:
                    return h_cost
                if c.weight<=left_deficit*1.1:
                    left_deficit -= c.weight
                    h_cost += 1
                    left_sum += c.weight
                    right_sum -= c.weight

        elif max(left_deficit, right_deficit) == right_deficit:
            for c in left_c:
                if c.weight>=right_deficit*1.1:
                    continue
                if c.weight<=right_deficit*1.1:
                    right_deficit -= c.weight
                    h_cost += 1
                    left_sum -= c.weight
                    right_sum += c.weight
        
        # If after potential moves it is still unbalanced, then it is impossible
        score = min(left_sum,right_sum)/max(left_sum,right_sum) 
        if score>0.9:
            return True
        else:
            False

class CraneOperations:

    # Get vertical index of the topmost container in a column
    def getTopContainerPos(self, ship_state, h_index):
        for i in range(ship_state.sizeV-2, -1, -1):
            if ship_state.state[i][h_index].container:
                return i
        return None
            
    # Get vertical index of the topmost empty place in a column
    def getTopColumnPos(self, ship_state, h_index):
        for i in range(ship_state.sizeV-2, -1, -1):
            if ship_state.state[i][h_index].container or ship_state.state[i][h_index].nan:
                return i+1
        return 0
            
    # Move Crane Horizontally to horizontal position h
    def operate(self, ship_state, h):
        top_container = self.getTopContainerPos(ship_state, h)
        if top_container == None:
            return
        original_v = ship_state.crane_v
        original_h = ship_state.crane_h

        # find containers/nan in the range of where the crane is and the target
        heightNeeded = ship_state.crane_v
        for c in ship_state.containers:
            if (c.container or c.nan) and c.y in range(min(ship_state.crane_h+1, h),max(ship_state.crane_h+1, h)):
                if c.x+1>heightNeeded:
                    heightNeeded = c.x+1
        targetColumnH = self.getTopColumnPos(ship_state, h)
        if heightNeeded<targetColumnH:
            heightNeeded = targetColumnH

        # Update Crane
        crane = ship_state.state[ship_state.crane_v][ship_state.crane_h]
        crane.name = 'UNUSED'
        ship_state.state[heightNeeded][h].name = 'CRANE' 
        ship_state.crane_movement_cells += manhattan(original_h, original_v, h, heightNeeded)
        ship_state.crane_h = h
        ship_state.crane_v = heightNeeded

        # ship_state.solution.append(str(original_v)+ str(original_v)+' to '+str(ship_state.crane_v)+str(ship_state.crane_h))
        # ship_state.solution.append('('+str("%02d"%original_v)+','+str("%02d"%original_v)+')('+str("%02d"%ship_state.crane_v)+','+str("%02d"%ship_state.crane_h)+') CRANE')
        # ship_state.solution.append('('+str("%02d"%original_v)+','+str("%02d"%original_v)+')('+str("%02d"%ship_state.crane_v)+','+str("%02d"%ship_state.crane_h)+') CRANE')
        # ship_state.solution.append('\tDEBUG ONLY - COST = '+str(manhattan(original_h, original_v, h, heightNeeded)))

    # Move Crane down from current position and move container to horizontal position h
    def operateH(self, ship_state, h):
        top_container = self.getTopContainerPos(ship_state, ship_state.crane_h)
        if top_container is not None and (ship_state.crane_h != h) and self.getTopColumnPos(ship_state, h)<8: # if there is a container at current crane horizontal position, attempt to move to h

            # set crane var
            original_v = ship_state.crane_v
            original_h = ship_state.crane_h
            # set container var
            containerH = ship_state.crane_h
            containerV = top_container
            container_to_move = ship_state.state[containerV][containerH]
            # set target space var
            targetH = h
            targetV = self.getTopColumnPos(ship_state, h)
            space = ship_state.state[targetV][targetH]
            
            # calculate manhattan 
            total_cost = 0

            # find from crane to top of container to move
            total_cost += manhattan(ship_state.crane_h, ship_state.crane_v, container_to_move.y, container_to_move.x+1)

            # find extra height needed to move container (to prevent container hitting any obstacles)
            heightNeeded = container_to_move.x
            for c in ship_state.containers:
                if (c.container or c.nan) and c.y in range(min(container_to_move.y+1, h), max(container_to_move.y+1, h)):
                    if c.x+1>heightNeeded:
                        heightNeeded = c.x+1
            targetColumnH = self.getTopColumnPos(ship_state, h)
            if heightNeeded<targetColumnH:
                heightNeeded = targetColumnH

            # total_cost += heightNeeded-container_to_move.x
            total_cost += manhattan(container_to_move.y, heightNeeded, container_to_move.y, container_to_move.x)
            
            #find from container to target space
            total_cost += manhattan(space.y, space.x, container_to_move.y, heightNeeded)
            ship_state.crane_movement_cells += total_cost

            # switch containers
            ship_state.state[containerV][containerH] = space
            ship_state.state[targetV][targetH] = container_to_move
            # update attributes in containers
            container_to_move.x = targetV
            container_to_move.y = targetH
            # container_to_move.container = False
            space.x = containerV
            space.y = containerH
            # space.container = True

            # update crane position
            crane = ship_state.state[ship_state.crane_v][ship_state.crane_h]
            crane.name = 'UNUSED'
            try:
                ship_state.state[targetV+1][targetH].name = 'CRANE' # crane is 1 higher than where the container is now
            except:
                print("try")
            ship_state.crane_h = targetH
            ship_state.crane_v = targetV+1

            ship_state.solution.append('('+str("%02d"%(containerV+1))+','+str("%02d"%(containerH+1))+')('+str("%02d"%(container_to_move.x+1))+','+str("%02d"%(container_to_move.y+1))+') '+str("%04d"%ship_state.crane_movement_cells)+' '+str(container_to_move.name)) # Manifest Format
            # ship_state.solution.append('('+str("%02d"%containerH)+','+str("%02d"%containerV)+')('+str("%02d"%container_to_move.y)+','+str("%02d"%container_to_move.x)+') '+str(container_to_move.name)) # Horizontal First

# Helper function to remove numpy array from list
def remove_np_array(list_input, arr):
    for i in range(len(list_input)):
        if list_input[i] == arr:
            list_input.pop(i)
            return
    print('ARR NOT FOUND')
            

class CargoSearch:
    frontier = PriorityQueue()
    frontier_list = [] # Just to iterate
    explored = [] # np.isin(obj, explored)

    bop = BalanceOperations()
    cop = CraneOperations()

    # AStar Search to find steps to balance ship
    def search(self, ship_state, manifest_link):
        start_time = time.time()

        self.frontier.queue.clear()
        self.frontier_list.clear()
        self.explored.clear()

        ship_state.load_state(manifest_link)
        self.bop.checkBalance(ship_state)
        if not self.bop.Possible(ship_state):
            print('IMPOSSIBLE TO BALANCE, PERFORMING SIFT')
            return self.SIFT(ship_state, manifest_link)

        self.frontier.put(ship_state) 
        self.frontier_list.append(ship_state)

        print('INITIAL STATE: \n')
        ship_state.print_state()
        print('\n\n')

        count = 0
        while not self.frontier.empty():
            # count+=1
            # if count == 2:
            #     return 0
            cur = self.frontier.get() #gets top of queue and pops
            remove_np_array(self.frontier_list, cur)

            # print("State to expand:", cur)
            # cur.print_state()

            #CHECK FOR GOAL
            self.bop.checkBalance(cur)
            if cur.balanced:
                print("---SOLUTION FOUND---")
                cur.print_state()
                print("\nSEARCH REVIEW")
                print("Depth: ",cur.depth)
                print("Total Time: ", time.time() - start_time)
                # cur.OutputManifest()
                return cur
            
            self.explored.append(cur)

            for i in range(12):

                # Create Copy of Cur
                temp=copy.deepcopy(cur)
                temp.increment_depth()

                # Apply operators
                # Search nodes split into two stages: 
                # - First stage is to move crane to position above a container (holdsContainer is False)
                # - Second stage is to move container to a position (holdsContainer is True)
                if temp.holdsContainer:
                    self.cop.operateH(temp, i)
                    temp.holdsContainer = False
                else:
                    self.cop.operate(temp, i)
                    temp.holdsContainer = True

                # Check if explored
                isExplored = False
                if any(np.array_equal(temp, x) for x in self.explored):
                    isExplored = True
                else:
                    isExplored = False

                # Check if in frontier
                inFrontier = False
                if any(np.array_equal(temp, x) for x in self.frontier_list):
                    inFrontier = True
                else:
                    inFrontier = False
                # Expand if not explored
                if not isExplored and not inFrontier:
                    self.frontier.put(temp)
                    self.frontier_list.append(temp)

        print("---NO SOLUTION FOUND---")
        print("Total time: ", time.time() - start_time)
        return 0
    
    # AStar Search to achieve the goal state of SIFT if it is impossible to balance
    def SIFT(self, ship_state, manifest_link):
        start_time = time.time()

        self.frontier.queue.clear()
        self.frontier_list.clear()
        self.explored.clear()

        ship_state.load_state(manifest_link)
        ship_state.sift = True
        self.bop.checkBalance(ship_state)

        self.frontier.put(ship_state)
        self.frontier_list.append(ship_state)

        print('INITIAL STATE: \n')
        ship_state.print_state()
        print('\n\n')

        count = 0
        while not self.frontier.empty():
            # count+=1
            # if count == 2:
            #     return 0
            cur = self.frontier.get() #gets top of queue and pops
            remove_np_array(self.frontier_list, cur)

            print("State to expand:", cur)
            cur.print_state()

            #CHECK FOR GOAL
            self.bop.checkBalance(cur)
            if cur.checkSift():
                print("---SOLUTION FOUND---")
                cur.print_state()
                print("\nSEARCH REVIEW")
                print("Depth: ",cur.depth)
                print("Total Time: ", time.time() - start_time)
                # cur.OutputManifest()
                return cur
            
            self.explored.append(cur)

            for i in range(12):
                # Create Copy of Cur
                temp=copy.deepcopy(cur)
                temp.increment_depth()
                # Apply operators
                if temp.holdsContainer:
                    self.cop.operateH(temp, i)
                    temp.holdsContainer = False
                else:
                    self.cop.operate(temp, i)
                    temp.holdsContainer = True
                # Check if explored
                isExplored = False
                if any(np.array_equal(temp, x) for x in self.explored):
                    isExplored = True
                else:
                    isExplored = False
                # Check if in frontier
                inFrontier = False
                if any(np.array_equal(temp, x) for x in self.frontier_list):
                    inFrontier = True
                else:
                    inFrontier = False
                # Expand if not explored
                if not isExplored and not inFrontier:
                    self.frontier.put(temp)
                    self.frontier_list.append(temp)

        print("---NO SOLUTION FOUND---")
        print("Total time: ", time.time() - start_time)
        return 0



            
# test_bop = BalanceOperations()
# test_search = CargoSearch()
# test_state = ShipState()

# Profiler: https://stackoverflow.com/questions/47836998/making-cprof-give-only-the-10-most-time-consuming-tasks-or-sort-them-by-time-in

# p = cProfile.Profile()
# p.enable()

# test_search.search(test_state, "Balance\ShipCase1.txt")
# test_search.search(test_state, "Balance\ShipCase2.txt")
# test_search.search(test_state, "Balance\ShipCase3.txt")
# test = test_search.search(test_state, "Balance\ShipCase4.txt")
# print('SOL: ', test.solution)
# test_search.search(test_state, "Balance\ShipCase5.txt")

# p.disable()
# stats = Stats(p)
# stats.sort_stats('tottime').print_stats(10)

# test_state.load_state("Balance\ShipCase5.txt")
# test_state.getHeuristicSift()
    
