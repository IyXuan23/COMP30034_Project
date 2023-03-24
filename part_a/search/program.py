# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from queue import PriorityQueue

def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    #Note to self: 
    #(r, q) are the coords of the cell
    #(dr, dq) are the directions the cell will spread to
    #(p, k) is the state, p being (b for blue, r for red), and k being the power of the current cell
    #in the game we are red
    
    #directions:
    # (0,1) = down-right
    # (-1,1) = downwards
    # (-1,0) = down-left
    # (0,-1) = up-left
    # (1,-1) = upwards
    # (1,0) = up-right

    #set up a priority queue
    pq = PriorityQueue()
    root = boardstate(input)
    #since root will be the only initial node, the priority is unimportant
    pq.put((0, root))

    if pq.empty():
        print("Cannot find route, or error has occured")
        return None
    
    currNodePair = pq.get()
    currNode = currNodePair[1]
    print("root configuration: ")
    print(currNode.board)

    #if game is complete, reconstruct the current path and moves and return it
    if gameFinish(currNode.board):
        
        #temporary placeholder
        print("completed")

    else:
        expandNodes(currNode, pq)

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]

class boardstate:
    """
    This class will be used to store the nodes of the tree, where board will
    be corresponding on the current boardstate, and paretNode will be the pointer
    to the previous node that the node was branched from
    """

    def __init__(self, board=None):

        #self.dataval here will contain the boardstate as a dictionary
        self.board = board
        #parentNode will be the previous node, used for reconstruction of the steps needed to win the game
        self.parentNode = None
        
        
        
def gameFinish(input: dict[tuple, tuple]) -> bool:
    """
    This function will check for whether the game has finished, ie. whether
    there are any more blue cells left within the board, returning false if there
    are and true otherwise
    """

    for cell in input.values():
        if "b" in cell:
            return False     

    return True    

def expandNodes(currNode: boardstate, pq: PriorityQueue()):

    chosenCellCoord = selectOptimalCell(currNode)

    #spread the cell in 6 directions, however we will give the direction that overtakes the
    #most opponent cells highest priority
    #for i in range(0,6):

        

def selectOptimalCell(currNode: boardstate) -> list:
    """
    This function is used to select the cell we will spread amongst the several cells
    we control. It uses a heuristic to calculate the cell with the best chances
    by including both power of the cell and distance to opposing cells within the
    heuristic, and returns the coordinates of the chosen cell
    """
    
    coords = []
    heuristicScore = -1

    #go through the dict until we find a red cell
    print("begin optimal cell selection:")
    for cell in currNode.board.items():
        if "r" in cell[1]:
            
            #for this heurisitc, we will calculate the reach of the cell
            #using its power, and check how many opposing cells are within its reach
            #and expanding the cell with the most amount of opposing cells within its reach

            currCellCoords = cell[0]
            currCellPower = cell[1][1]

            numCellsInRange = 0

            #check how many blue cells our current red cell can spread to
            for cell2 in currNode.board.items():
                if "b" in cell2[1]:

                    if cellInRange(currCellCoords, cell2[0], currCellPower):
                        numCellsInRange += 1
                
            if (numCellsInRange > heuristicScore):
                heuristicScore = numCellsInRange
                coords = currCellCoords
                print(coords)
                print(heuristicScore)

    return coords            

def cellInRange(currCellCoords: tuple, oppCellCoords: tuple, currCellPower: int) -> bool:

    """
    This function will calculate whether a specific cell is within range
    of another cell, by calculating whether the power is sufficient to 
    overwrite the opposing cell when using SPREAD
    """
    
    #checking for movement along the r-axis
    if ((currCellCoords[1] == oppCellCoords[1]) and \
        (abs(currCellCoords[0] - oppCellCoords[0]) <= currCellPower)):
        return True
    
    #checking for movement along the q-axis
    if ((currCellCoords[0] == oppCellCoords[0]) and \
        (abs(currCellCoords[1] - oppCellCoords[1]) <= currCellPower)):
        return True
    
    #checking for movement vertically and horizontally

    #if the column has total sum of n < 6, it can spread to columns with total sum n+7
    #vice versa, if n > 6, it can spread to columns with total sum n-7
    #if n==6, then it can only spread to columns with n==6
    #(due to the nature of the infinite board)

    currCoordSum = currCellCoords[0] + currCellCoords[1]
    currOppSum = oppCellCoords[0] + oppCellCoords[1]

    if ((currCoordSum == currOppSum) or (abs(currCoordSum - currOppSum) == 7)):
        if (abs(currCellCoords[0] - oppCellCoords[0]) <= currCellPower):
            return True
        
    return False    