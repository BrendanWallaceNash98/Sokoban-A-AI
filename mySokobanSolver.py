
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
import itertools

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(9993304, "Brendan", "Wallace-Nash"),(9300449, "Min-Pu", "Tsai"), (10661450, "Bingqing", "Qian")]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 

    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.

    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.

    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"    



    #This code will use the taboo_cells_loc() function to 
    #output a 
    taboo = taboo_cells_loc(warehouse)
    X,Y = zip(*warehouse.walls)
    x_size = max(X)+1
    y_size = max(Y)+1    
    wh_string = [([" "] * x_size)for y in range(y_size)]
    for (x,y) in warehouse.walls:
        wh_string[y][x] = "#"
    for cell in taboo:
        wh_string[cell[1]][cell[0]] = "X"

    return "\n".join(["".join(line) for line in wh_string])

def taboo_cells_loc(warehouse):
    '''
    this function is used to return the mark_taboo_cells function
    with the correct parameters. the function declares the visted list
    returned from the get_licit_cells function to the variable licit_cells.

    @param warehouse: the warehouse object is pased as a parameter

    @return:
        This function will return all the taboo cells locations
        of the given warehouse by returning the mark_taboo_cells
        function with the warehouse and licit_cells passed as parameters
    '''
    licit_cells = get_licit_cells(warehouse)
    return mark_taboo_cells(warehouse, licit_cells)


def mark_taboo_cells(warehouse, visted):
    '''
    this function will find and return all the taboo cells in the warehouse that is passed
    taboo cells are only reported if they reside within an area the worker can get to. There
    are some warehouses were there are areas with taboo cells but they do not reside within the parts
    of the warehouse the worker can get to (example in warehouse 185). 

    @param warehouse: a Warehouse object, valid_cell: a list of valid cells where the worker can go

    @return
        a list of taboo locations within the given warehouse
    '''
    #this code will take out all the targets from the warehouse
    for target_cell in warehouse.targets:
        visted.discard(target_cell)

    #this will find all the corners and add them to taboo_list
    taboo_list = set([cell for cell in visted 
               if (get_adjacent_cells(cell)['top'] in warehouse.walls and get_adjacent_cells(cell)['left'] in warehouse.walls)or
               (get_adjacent_cells(cell)['bottom'] in warehouse.walls and get_adjacent_cells(cell)['left'] in warehouse.walls)or
               (get_adjacent_cells(cell)['top'] in warehouse.walls and get_adjacent_cells(cell)['right'] in warehouse.walls)or
               (get_adjacent_cells(cell)['bottom'] in warehouse.walls and get_adjacent_cells(cell)['right'] in warehouse.walls)])

    # this code segment will mark the taboo cells if they 
    # reside between two coners and along a wall by using
    #the list of corners in the taboo_list
    taboo_alongWall = set()
    for cell_1, cell_2 in itertools.combinations(taboo_list, 2): 
        x_1 = cell_1[0]
        y_1 = cell_1[1]
        x_2 = cell_2[0]
        y_2 = cell_2[1]

        # this code is to determine if the two corners make a verticle wall
        if x_1 == x_2:
            if y_1 > y_2:
                y_1 = y_2
                y_2 = y_1
            # check whether there is a target or wall (obsticle) between them
            # if there is a target the loop is broken and its coordinates
            # is not added to the taboo_list
            obstacle = False
            for y in range(y_1+1,y_2):
                if (x_1,y) in warehouse.targets or (x_1,y) in warehouse.walls:
                    obstacle = True
                    break
            if obstacle:
                continue

            #the code segment assigns taboo cells if they are found to be along a verticle 
            #wall. This done by looping over the range of the two y coordinates and if the -1  
            #or +1 (depending on L or R) X value is not in a warehouse.wall 
            #then it is not added to taboo_wall
            for y in range(y_1, y_2+1):
                if (x_1-1, y) not in warehouse.walls:
                    taboo_wall_left = True
                else:
                    taboo_wall_left = False

            for y in range(y_1, y_2+1):
                if (x_1+1, y) not in warehouse.walls:
                    taboo_wall_right = True
                else:
                    taboo_wall_right = False


            #both left and right taboo wall cells are merged into taboo_alongWall
            if taboo_wall_left or taboo_wall_right:
                taboo_alongWall |=  set([(x_1, y) for y in range(y_1+1, y_2)])

        # this code is to determine if the two corners make a horizontal wall
        if y_1 == y_2:
            if x_1 > x_2:
                x_1 = x_2
                x_2 = x_1
            # check whether there is a target or wall (obsticle) between them
            # if there is a target the loop is broken and its coordinates
            # is not added to the taboo_list
            obstacle = False
            for x in range(x_1+1,x_2):
                if (x,y_1) in warehouse.targets or (x,y_1) in warehouse.walls:
                    obstacle = True
                    break
            if obstacle:
                continue

            #the code segment assigns taboo cells if they are found to be along a horizontal
            #wall. This done by looping over the range of the two x coordinates and if the -1  
            #or +1 (depending on top or bottom) of the y value is not in a warehouse.wall 
            #then it is not added to taboo_wall                           
            for x in range(x_1, x_2+1):
                if (x+1, y_1-1) not in warehouse.walls:
                    taboo_wall_top = True 
                else:
                    taboo_wall_top = False

            for x in range(x_1, x_2+1):
                if (x, y_1+1) not in warehouse.walls:
                    taboo_wall_bottom = True
                else:
                    taboo_wall_bottom = False


            # append all dead end cells along the wall into set
            if taboo_wall_top or taboo_wall_bottom:
                taboo_alongWall |= set([(x,y_1) for x in range(x_1+1, x_2)])      

    #both top and bottom taboo wall cells are merged into taboo_alongWall
    taboo_list |= taboo_alongWall

    return taboo_list


def get_licit_cells(warehouse):
    '''
    this function is used to establish all the licit cells that
    are within the bounds of the warehouse. The warehouse.worker
    is used as a starting point and then the get_adjacent_cells
    function is used looped over to until all the licit cells in the 
    warehouse are found. all the licit cells are stored in the visited
    list.

    @param warehouse: a Warehouse object

    @return 
        the function returns a list of licit cells contained in the 
        licit list.
    '''

    start,visted = set(), set()
    start.add(warehouse.worker)

    while start:
        location = start.pop()
        visted.add(location)

        adjacent_cells = get_adjacent_cells(location)

        for adjacent_cell in adjacent_cells.values():
            if (adjacent_cell not in start and adjacent_cell not in visted and adjacent_cell not in warehouse.walls):
                start.add(adjacent_cell)
    return visted

def get_adjacent_cells(location):
    '''
    this function is used to find the adjacent cells of the start location
    for the warehouse.worker in the get_ilicit_cells function

    @param location: the initial cell of the warehouse.worker's location

    @return:
        the returned dictionary contains all the locations of the adjacent cells
    '''

    loc_x, loc_y = location
    right_loc = loc_x+1, loc_y
    left_loc = loc_x-1, loc_y
    top_loc = loc_x, loc_y+1
    bottom_loc = loc_x, loc_y-1
    return {'right':right_loc,'left':left_loc,
                'top':top_loc,'bottom':bottom_loc}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes
    
    #this is the contructer used for the sokoban class
    def __init__(self, initial=None, allow_taboo_push=True, macro=False, weights=None):
        self.initial = initial.__str__()
        self.wh = initial
        self.goal = initial.copy(boxes=initial.targets).__str__()
        self.boxLoc = initial.boxes
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro
        self.weights = weights
        

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        
        @param: self and state
    
        @return 
            this function returns a list of allowed actions that can be preformed in the current state
        """
        #locations extracted from warehoue
        self.wh.extract_locations(state.split(sep="\n"))
        allowed_actions = []
        #taboo cell locations from the mark_taboo_cells function are added
        taboo = mark_taboo_cells(self.wh, get_licit_cells(self.wh))
        for move in (UP, RIGHT, DOWN, LEFT):
            #if self.macro is true this code will execute
            if self.macro:
                #loop will run for number of boxes in the self.wh
                for wh_box in self.wh.boxes:
                    #new box location establisehed
                    next_loc = move.move_loc(wh_box)
                    #establish worker location
                    worker_loc = (wh_box[1] - 1 * move.heap[1], wh_box[0] - 1 * move.heap[0])
                    #if worker(worker_loc) and box(next_loc) are not in a wall, and box not
                    #in one of the other boxes in self.boxes then the move is added to 
                    #allowed_actions
                    if worker_loc and next_loc not in self.wh.walls and next_loc not in self.wh.boxes:
                        if self.allow_taboo_push:
                            allowed_actions.append((wh_box, move))
                        #if next_loc box move is not in a taboo cell it will also be allowed
                        else:
                            if next_loc not in taboo:
                                allowed_actions.append((wh_box, move))
            # if not self.macro this code will execute              
            else:
                first_worker = self.wh.worker
                second_worker = self.wh.worker
                first_worker = move.move_loc(first_worker)
                second_worker = move.move_loc(first_worker)
                #if first_worker is in a box and second_worker is not in a box or wall
                #and allow_taboo_push is true then move will be added to allowed move
                #if allow_taboo_push is not true the move will only be added if not in
                #taboo
                if first_worker in self.wh.boxes and second_worker not in self.wh.boxes and second_worker not in self.wh.walls:
                    if self.allow_taboo_push:
                        allowed_actions.append(move)
                    else:
                        if second_worker not in taboo:
                            allowed_actions.append(move)
                #if first worker is not in a wall or box it is added to allowed_action
                if first_worker not in self.wh.boxes and first_worker not in self.wh.walls:
                    allowed_actions.append(move)
        return allowed_actions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        
        @param warehouse: self, state, action
    
        @return 
        the function returns a state in string format that resulted from executing one of the 
        actions from the action function for its given state
        """
        #locations are extracted from self.wh
        self.wh.extract_locations(state.split(sep="\n"))
        #if macro is true location will be equal to action[0]
        if self.macro:
            location = action[0]
            #if location is in a box location then this code will run
            if location in self.wh.boxes:
                self.wh.boxes.remove(location)
                self.wh.worker = location
                new_location = action[1].move_loc(location)
                self.wh.boxes.append(new_location)
        #if macro is false this code will run
        else:
            first_loc = self.wh.worker
            second_loc = self.wh.worker
            first_loc = action.move_loc(first_loc)
            second_location = action.move_loc(first_loc)
            if first_loc in self.wh.boxes and second_location not in self.wh.boxes and second_location not in self.wh.walls:
                    self.wh.boxes.remove(first_loc)
                    self.wh.boxes.append(second_location)
            self.wh.worker = first_loc
        return self.wh.__str__()

    def goal_test(self, state):
        """
        This function will return true if the goal is the same as the state.
        
        @param warehouse: self, state
    
        @return 
        this function will return true if the state is the goal
        
        """
        #boxes from the state are compared against targets from goal and if they are equal goal_test
        #returns true
        state_wh = sokoban.Warehouse()
        state_wh.extract_locations(state.split(sep="\n"))
        goal_wh = sokoban.Warehouse()
        state_boxes = state_wh.boxes
        goal_wh.extract_locations(self.goal.split(sep="\n"))
        goal_target = goal_wh.targets
        return set(state_boxes) == set(goal_target)
    

    def path_cost(self, c, state, action, state2):
        """
        this function will return the cost of the solution path that arrives from state1 
        to state2 by using the action function. the defualt is that c is equal to 1 but the cost 
        will be added to the weight if the boxes have any weights
        
        
        @param warehouse: self, c = cost, state, action, state2 
    
        @return 
        this function will return the cost of the path taken by the worker
        
        """
        #load and extract
        wh2 = load_extract(self,state2)
        #if self weights are none defualt cost will be used
        if self.weights == None:
            return c + 1
        #if wieghts are not noe then this code will 
        #reurun the cost with the weights
        else:
            for i in range(len(self.boxLoc)):
                if self.boxLoc[i] not in wh2.boxes:
                    box_weight = self.weights[i]
                    for box in wh2.boxes:
                        if box not in self.boxLoc:
                            self.boxLoc[i] = box
                        return c + 1 + box_weight

    def h(self, n):
        """
        this function will establish the heuristic. If the boxes weights are none the heurisitic
        will be zero + the manhattan distance. If the boxes have wights then the heuristic should calcualte 
        the manhattan distance from each box to each target and times it by the boxes weight. The paths with the
        lowest total manhattan distance cost should be used.
        
        @param warehouse: self,n 
    
        @return 
        this function will return the best heuristic for the algorithim to use
        
        """
        heuristic = 0
        wh = sokoban.Warehouse()
        wh.extract_locations(n.state.split(sep="\n"))
        if self.weights == None:
            for box in wh.boxes:
                wh_target = wh.targets[0]
                for target in wh.targets:
                    if(manhattan_distance(target, box) < manhattan_distance(wh_target, box)):
                        wh_target = target
                heuristic = heuristic + manhattan_distance(wh_target, box)

            return heuristic
        else: 
            for box in wh.boxes:
                if box.wieghts == wh.weights[1]:
                    for target in wh.targets:
                        if(manhattan_distance(target, box) < manhattan_distance(wh_target, box)):
                            wh_target = target
                        heuristic = heuristic + manhattan_distance(wh_target, box)

                        return heuristic
                else:

                    wh_target = wh.targets[1]
                    wh_weights = self.weights[1]
                    for target, i in wh.targets, self.weights[i]:
                        if(manhattan_distance(target, box)*self.weights[i] < manhattan_distance(wh_target, box)*wh_weights):
                            wh_target = target
                            heuristic = heuristic + manhattan_distance(wh_target, box)

                            return heuristic

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    #Forbiden:
    #1. player try to push multiple boxes
    #2. player try to push box in wall
    #3. player try to get into wall
    #
    ##
    #Todo:
    #1. Return 'Impossible' if fprbiden
    #2. Return 
    
    #worker position:
    worker_x, worker_y = warehouse.worker
    movement = 1
    
    #Switch Cases:
    def action_up():
        return (worker_x, worker_y-movement)
    def action_down():
        return (worker_x, worker_y+movement)
    def action_right():
        return (worker_x+movement, worker_y)
    def action_left():
        return (worker_x-movement, worker_y)
    def Default():
        return (worker_x, worker_y)    
    actionDict = {
        'Up': action_up,
        'Down': action_down,
        'Right': action_right,
        'Left': action_left,
        }
    
    #Return the location forward the input direction.
    def getAction(action):
        position = actionDict.get(action, Default) #return coordinate otherwise Default.
        return position
    
    #traverse the input action sequence
    for action in action_seq:        
        forward_tile = getAction(action)() 
        #if a wall in front of moving direction, return 'Impossible'.
        if(forward_tile in warehouse.walls): 
            return 'Impossible'
        
        #the further forward tile is the tile one movement away from forward_tile.
        movement+=1
        further_forward_tile = getAction(action)()
        
        #check if the box in front of player against the wall or another box. 
        #if so, return 'Impossible'; otherwise push the box. 
        if(forward_tile in warehouse.boxes):
            if(further_forward_tile in warehouse.boxes or further_forward_tile in warehouse.walls):
                return 'Impossible'
            warehouse.boxes.remove(forward_tile)
            warehouse.boxes.append(further_forward_tile)
        
        # change the pointer back to one, which point to tile right in front.
        movement-=1 
        # it's a legal move, so move.
        worker_x, worker_y = forward_tile 
            
    warehouse.worker = (worker_x, worker_y)    
    return warehouse.__str__()
            
    #raise NotImplementedError()




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    ''''
    using the weighted sokoban puzzle, if there is no weights of the boxes the boxes should go 
    to their respective closest target. If the boxes are weighted the A star algorithim
    should move the boxes so that heavier boxes are given priority to closer targets.
    This will reduce the the total cost of the path as heavier boxes will be moved less
    creating less of a penalty.
    @param 
     warehouse: a valid Warehouse object
    @return
        the function will return impossible if it cannot be solved.
        
        the function will return the action sequence and cost of movements
        for the boxes to reach their target if it can be solved.
        
        the function will retur  [] if the warehouse is already in goal state
        
    '''

    puzzle = SokobanPuzzle(warehouse)

    wh_copy = warehouse.copy()
    if (wh_copy.boxes == wh_copy.targets):
        return []
    puzzle_search = search.astar_graph_search(puzzle, puzzle.h)
    move = []
    move_cost = []
    if (puzzle_search is None):
        return 'Impossible'
    else:
        for node in puzzle_search.path():
            move.append(node.action.__str__())
            move_cost.append(node.path_cost)
        action_seq = move[1:]
        cost = max(move_cost)

        if check_elem_action_seq(wh_copy, action_seq) == 'Impossible':
            return 'Impossible'
        else:
            return action_seq, cost


# - - - - - - - - - - - -other functions - - - - - - - - - - - - - - - - - - - - - - - - - - -
def manhattan_distance(first_location, second_location):
    '''
        this function is used to calculate the manhattan distance 
        between two locations
        
        @params: first_location = initial location, secound_location = goal_location
        
        @return: the fucntion will return the mahattan distance between the two locations.
        
    '''
    return abs((first_location[0] - second_location[0])) + abs((first_location[1] - second_location[1]))


def load_extract(self, state):
    wh = sokoban.Warehouse()
    return wh.extract_locations(state.split(sep="\n"))

class Pointer:
    

    def __init__(self, pointer_name, heap):

        self.pointer_name = pointer_name
        self.heap = heap

    def move_loc(self, position):

        return (position[0] + self.heap[0], position[1] + self.heap[1])

    def __str__(self):

        return str(self.pointer_name)
        
    def heap(self):

        return self.heap

    



UP = Pointer("Up", (0, -1))
DOWN = Pointer("Down", (0, 1))
RIGHT = Pointer("Right", (1, 0))
LEFT = Pointer("Left", (-1, 0))

