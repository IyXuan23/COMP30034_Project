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
    
    while not pq.empty():

        currNodePair = pq.get()
        currNode = currNodePair[1]
        print("root configuration: ")
        print(currNode.board)

        #if game is complete, reconstruct the current path and moves and return it
        if gameFinish(currNode.board):
        
            #temporary placeholder
            print("Solution Found")
            SequenceList = []
            SequenceList = retraceSteps(currNode, SequenceList)
            print(SequenceList)
            break

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
        #lastMove will record the last used move in the sequence, to be used in reconstruction of the
        #game-winning sequence of moves
        self.lastMove = None
        #number of moves that have been carried out
        self.NumOfMoves = 0

    #used if priority of the 2 cells are the same, we shall compare their total cell powers
    #DO NOT DELETE, WILL CAUSE ERROR xD
    def __eq__(self, other):

        totalSelfPower = 0
        totalOtherPower = 0

        for cell in self.board.items():
            if "r" in cell[1]:
                totalSelfPower+= cell[1][1]
        for cell in other.board.items():
            if "r" in cell[1]:
                totalOtherPower+= cell[1][1]
        return totalOtherPower == totalSelfPower


    def __lt__(self, other):

        totalSelfPower = 0
        totalOtherPower = 0

        for cell in self.board.items():
            if "r" in cell[1]:
                totalSelfPower+= cell[1][1]
        for cell in other.board.items():
            if "r" in cell[1]:
                totalOtherPower+= cell[1][1]
        return totalOtherPower > totalSelfPower
        
        
def gameFinish(input: dict[tuple, tuple]) -> bool:
    """
    This function will check for whether the game has finished, ie. whether
    there are any more blue cells left within the board and red cells remaining, 
    returning false if there are and true otherwise
    """

    redCellsExist = False

    #if blue cells exist, game isn't over
    #alternatively, if there are no red cells, game is not won either, so return false
    for cell in input.values():
        if "b" in cell:
            return False     
        if "r" in cell:
            redCellsExist = True

    if redCellsExist:
        return True
    else:
        return False    

def expandNodes(currNode: boardstate, pq: PriorityQueue()):

    """"This function will expand the node by a factor of 6 (due to the nature
    of the hexagonal board) and assign each child node a priority, then add each
    node to the priority queue to continue the search"""

    chosenCellCoord = selectOptimalCell(currNode)
    #make a copy of the old boardstate that we will update to
    #generate the new board
    oldBoardState = currNode.board

    spreadPower = oldBoardState.get(chosenCellCoord)[1]

    #spread the cell in 6 directions, however we will give the direction that overtakes the
    #most opponent cells highest priority

    directions = ((0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1), (1, 0))
    for direction in directions:

        newBoardState = oldBoardState.copy()

        newCellCoord = chosenCellCoord
        newCellCoord = list(newCellCoord)
        chosenCellCoord = tuple(chosenCellCoord)


        #generate the new cells in the given direction, after which delete the original cell
        #that has been expended
        for i in range(0,spreadPower):
            
            #ensure that if we exit and re-enter the board, the coords update
            #correctly by not exceeding 7
            newCellCoord[0] = newCellCoord[0] + direction[0]
            if (newCellCoord[0] >= 7):
                newCellCoord[0] -= 7

            newCellCoord[1] = newCellCoord[1] + direction[1]
            if (newCellCoord[1] >= 7):
                newCellCoord[1] -= 7

            #if existing cell is in place, overwrite it and +1 to the existing power,
            #otherwise create a new cell in the spot
            if (newBoardState.get(tuple(newCellCoord)) == None):
                newBoardState[tuple(newCellCoord)] = ("r", 1)
            else:
                newPower = newBoardState.get(tuple(newCellCoord))[1] + 1
                newBoardState[tuple(newCellCoord)] = ("r", newPower)    

        #deleting original expended cell
        newBoardState.pop(chosenCellCoord)    

        newNode = boardstate(newBoardState)
        newNode.parentNode = currNode
        newNode.NumOfMoves = currNode.NumOfMoves + 1
        newNode.lastMove = ("SPREAD", chosenCellCoord, direction)

        #temporary placeholder of priority 1 for testing ???

        priorityScore = generatePriority(newNode)

        pq.put((priorityScore, newNode))


def generatePriority(newNode: boardstate) -> int:
    """
    This function will generate a priority to assign to the given node, by calculating the euclidean
    distance between the red and blue cells. In the event of mulitple red cells, we will use the 
    distance of the closest red cell to generate the distance
    """        

    priorityScore = 0

    #iterate through blue cells, and find the closest red cell, then take the
    #distance between the 2, and add it to the total score
    for blueCell in newNode.board.items():
        if "b" in blueCell[1]:

            closestDistance = -1

            for redCell in newNode.board.items():    
                if "r" in redCell[1]:

                    euclideanDistanceR = abs(blueCell[0][0] - redCell[0][0])
                    euclideanDistanceQ = abs(blueCell[0][1] - redCell[0][1])
                    euclideanDistanceTotal = euclideanDistanceR + euclideanDistanceQ

                    if euclideanDistanceTotal > closestDistance:
                        closestDistance = euclideanDistanceTotal

            priorityScore += closestDistance    
    
    return priorityScore



def selectOptimalCell(currNode: boardstate) -> list:
    """
    This function is used to select the cell we will spread amongst the several cells
    we control. It uses a heuristic to calculate the cell with the best chances
    by including both power of the cell and distance to opposing cells within the
    heuristic, and returns the coordinates of the chosen cell
    """
    #coords of the chosen cell
    coords = []
    #negative value will ensure all generated scores will be greater that -1
    heuristicScore = -1

    #go through the dict until we find a red cell
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

            #replace cell if current cell is superior in score    
            if (numCellsInRange > heuristicScore):
                heuristicScore = numCellsInRange
                coords = currCellCoords

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

def retraceSteps(currNode: boardstate, SequenceList: list) -> list:

    """This function will go along the winning sequence, and return the list of winnning moves
    by referencing the parent nodes until the root is reached"""

    if currNode.lastMove == None:
        return SequenceList

    else:
        SequenceList.append(currNode.lastMove)
        SequenceList = retraceSteps(currNode.parentNode, SequenceList)
        return SequenceList


def generatePriority2(newNode: boardstate) -> int:
    """
    This function is a unused prototype of a A*star search, where
    f(x) = g(x) + h(x), where the g(x) is the amount of moves taken
    to reach the current point and h(x) is the euclidean distance between the 
    closest red and blue cells
    """        

    priorityScore = 0

    #since our goal is to find the minimum number of moves, the culmulative cost'
    #g(x) should take the highest weightage, so we assign each move a weightage of 1000
    priorityScore += newNode.NumOfMoves * 1000

    #iterate through blue cells, and find the closest red cell, then take the
    #distance between the 2, and add it to the total score
    for blueCell in newNode.board.items():
        if "b" in blueCell[1]:

            closestDistance = -1

            for redCell in newNode.board.items():    
                if "r" in redCell[1]:

                    euclideanDistanceR = abs(blueCell[0][0] - redCell[0][0])
                    euclideanDistanceQ = abs(blueCell[0][1] - redCell[0][1])
                    euclideanDistanceTotal = euclideanDistanceR + euclideanDistanceQ

                    if euclideanDistanceTotal > closestDistance:
                        closestDistance = euclideanDistanceTotal

            priorityScore += closestDistance    
    
    return priorityScore