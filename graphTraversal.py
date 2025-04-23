# Jason Rudinsky
# April 22, 2025
# Autonomous Mobile Robots - Grad project

# This is the code that will be used to traverse through a given graph using the various search methods,
# and the program will output the path taken from the start position to the end position of the various graphs to a file.
# The program will in a separate file also output the time it took to traverse said graph to the user as well.

# 4/22/2025 - Original Version
# 4/22/2025 @ 4:28 pm - Added some functionality when the user is choosing DFS or BFS. Created files to hold 
    # the paths returned from the search algorithms as well as the time taken to traverse the graphs. 
    # Also created some of the methods needed to compute the greedy search. 
    # Found and fixed a bug in my greedy implementation where I was entering a cycle.
    # Also abstracted the greedy method to make it so I could hopefully use it for UCS, and A* as well.
# 4/23/2025 - Finished making making it so that A* and UCS can both be called from the greedy method. 
    # Also added in a feature where I can call the program to perform calculations for each and every search method that was created.


import graphCreation, heapq, math                                                                           # Importing the various modules
from timeit import default_timer as timer                                                                   # Importing the timer



# This is the method that will be used as the hub for calling the different traversal methods. 
# This is where the program will write the information of the paths that were obtained via the 
# different traversal methods to the output file as well as writing the time it took to perform the traversals to its own file. 
def doTraversal(arguments):                                                                                 # Method Block
    
                                                                                                            # VARIABLE DEFINITIONS
                                                                                                            
    if len(arguments) != 2 and len(arguments) != 3:
        raise Exception("Attempted bypassing of main method! This should not be allowed")                   # Raises the error to the user

    if len(arguments) == 2:                                                                                 # If the user entered in one numerical value and the other being a traversal method
        row = col = int(arguments[0])                                                                       # Sets the value of row and col
        traversalMethod = arguments[-1].upper()                                                             # Sets the value of traversalMethod
    else:                                                                                                   # Two dimensions to look at
        row, col, traversalMethod = int(arguments[0]), int(arguments[1]), arguments[-1].upper()             # Sets the values of row, col, and traversalMethod
            
    
    #print(f"Looking for directory: Graphs/{row} by {col}")                                                  # Debug print statememnt
    if not graphCreation.os.path.exists(f"Graphs/{row} by {col}"):                                          # If the given path does not exist
        raise Exception(f"The path: \'Graphs/{row} by {col}\' does not exist within the current directory") # Raises the exception to the user
    
    folderLooky = graphCreation.os.listdir(f"Graphs/{row} by {col}")                                        # Obtains the files in the directory
    if len(folderLooky) == 0:                                                                               # Empty directory
        raise Exception(f"The directory \'Graphs/{row} by {col}\' has no graphs in the folder")             # Raises the exception to the user
    
    folderLooky = list(filter(lambda x: "graph" in x, folderLooky))
       
    folderLooky.sort()                                                                                      # Sorts the values in folderLooky

    acceptedMethods = ["DFS", "BFS", "GREEDY", "UCS", "A*"]                                                 # Defines the list of accepted traversal methods

    match traversalMethod:                                                                                  # Match case
        case "DFS":                                                                                         # Doing a DFS Search
            theFile = open(f"Graphs/{row} by {col}/DFS-Paths.txt", "w")                                     # Opens a new file
            fout = open(f"Graphs/{row} by {col}/DFS-Paths-Times.txt", "w")                                  # Opens the file
        case "BFS":                                                                                         # Doing a BFS Search
            theFile = open(f"Graphs/{row} by {col}/BFS-Paths.txt", "w")                                     # Opens a new file
            fout = open(f"Graphs/{row} by {col}/BFS-Paths-Times.txt", "w")                                  # Opens the file
        case "GREEDY":
            theFile = open(f"Graphs/{row} by {col}/Greedy-Paths.txt", "w")                                  # Opens a new file
            fout = open(f"Graphs/{row} by {col}/Greedy-Paths-Times.txt", "w")                               # Opens the file
        case "UCS":
            theFile = open(f"Graphs/{row} by {col}/UCS-Paths.txt", "w")                                     # Opens a new file
            fout = open(f"Graphs/{row} by {col}/UCS-Paths-Times.txt", "w")                                  # Opens the file
        case "A*":
            theFile = open(f"Graphs/{row} by {col}/Astar-Paths.txt", "w")                                   # Opens a new file
            fout = open(f"Graphs/{row} by {col}/Astar-Paths-Times.txt", "w")                                # Opens the file
        case "EVERYTHING!":
            for i in acceptedMethods:                                                                       # Looping for all the searches
                passingArgs = arguments[:-1]                                                                # Sets the value of passing args
                passingArgs.append(i)                                                                       # Appends the traversal method to the list
                doTraversal(passingArgs)                                                                    # Recursive call to method doTraversal
            return                                                                                          # Exits the method
            
        case _:                                                                                             # Default case
            raise Exception(f"The following traversal hasn't been implemented yet: {traversalMethod}")      # Raises error to the user

    for graphFile in folderLooky:                                                                           # For Loop
            
        graph = createGraph(f"Graphs/{row} by {col}/{graphFile}")                                           # Call to method createGraph
        #graphCreation.printList(graph)                                                                      # Debug print to make sure the graph is created correctly
        #print("")
        start = timer()                                                                                     # Starts the timer
        
        match traversalMethod:                                                                              # Match case
            case "DFS" | "BFS":                                                                             # Doing DFS or BFS traversal
                path = graphCreation.traversal(graph, traversalMethod == "DFS")                             # Calls the traversal method of graphCreation
            case "GREEDY" | "UCS" | "A*":
                path = greedy(graph, (traversalMethod == "GREEDY" or traversalMethod == "A*"), (traversalMethod == "UCS" or traversalMethod == "A*"))
                
        end = timer()
            
        theFile.write(f"{graphFile} {traversalMethod} Path:{path}\n")                                       # Writes to the path
        fout.write(f"{graphFile} {traversalMethod} time taken: {end - start} second(s)\n")                  # Writes the second time
    
    else:
        theFile.close()                                                                                     # Closes theFile
        fout.close()                                                                                        # Closes fout     
                
        
        
# This is the method that will be used to create the graph representation when given the appropriate file.
# Once the graph is created the graph will be returned to the user.    
def createGraph(graphFile):                                                                                 # Method Block
    
    fileInfo = []                                                                                           # Creates an empty list to store the info from the file
   
    fileData = open(graphFile, "r")                                                                         # Opens the file
   
    fileInfo = fileData.readlines()                                                                         # Reads the data from the file
    
    fileData.close()                                                                                        # Closes the input file
    
    gridDimensions = fileInfo[0].split()                                                                    # Retrieves the grid dimensions
   
    row = int(gridDimensions[0])                                                                            # Gets the row value for the grid
    column = int(gridDimensions[1])                                                                         # Gets the column value for the grid
   
    grid = [["-" for LCV in range(column)] for LCV2 in range(row)]                                          # Makes a row by column 2d Array
   
   
    for i, rowVal in enumerate(fileInfo[1:]):                                                               # For Loop
      
        # Removing spaces and new line characters
        # so only the values for the arrows remain
        infoForRow = rowVal.split()                                                                         # Removes the spaces from rowVal
      
        # Looping through the obtained list to place values into the 2d grid
        for j, val in enumerate(infoForRow):                                                                # For Loop
            grid[i][j] = val                                                                                # Sets the value at grid[i][j]
    
    else: return grid                                                                                       # Returns grid to the user
   
    

# This is the method that will be used to return the euclidean heuristic value.
# I have not decided whether or not to choose this or manhattan for the heuristic
# so both will be included until I make a decision
def manhattanHeuristic(currentState, terminalState):                                                                 # Method Block
   
                                                                                                                     # VARIABLE DEFINITIONS
   curXYPosition = currentState                                                                                      # Defines a variable to look at the values in the tuple currentState
   terminationXYPosition = terminalState                                                                             # Defines a variable to look at the values in the tuple terminalState
   
   # Manhattan = |x1 - x2| + |y1 - y2|
   return abs(curXYPosition[0] - terminationXYPosition[0]) + abs(curXYPosition[1] - terminationXYPosition[1])        # Returns the manhattan distance to the user
   


# This is the method that will be used to calculate the path traversal based on a greedy approach.
# It will use the manhattan heuristic function to calculate which would be the closest path to goal to go towards.
def greedy(graph, userHeuristic = True, backwardsCost = False):                                             # Method Block
    
                                                                                                            # VARIABLE DEFINITIONS
    rowIncrement, colIncrement = 0, 0                                                                       # Defines values for the row and column increments
    row, col = 0, 0                                                                                         # Defines values for the current values of row and col
    steps = 0                                                                                               # Defines a value for the number of steps taken
    path, arrowLooky = "", ""                                                                               # Defines a value for the path and arrowLooky
    pqueue = []                                                                                             # Data Structure to store the DFS traversal of the stack
    tempGraph = [[len(graph[0]) * len(graph) if backwardsCost == True else 0 for j in range(len(graph[0]))] for i in range(len(graph))]                             # Shorthand for creating the list

    startingCoor = (0, 0)                                                                                   # Sets the value of startingCoor
    endingCoor = (len(graph) - 1, len(graph[0]) - 1)                                                        # Sets the value of endingCoor
        
    startingPosition = [(0, 0), "", 0]                           # Defines the startingPosition
    pqueue.append(startingPosition)                                                                         # Appends the starting position to the user
    #graphCreation.printList(graph)
    #print(pqueue)
    
    while len(pqueue) != 0:                                                                                 # As long as we have coordinates to traverse
        #print(pqueue)
        curPos, path, cost = pqueue.pop(0)                                                                   # Pops from the front of the queue
                
        rowIncrement, colIncrement, arrowLooky = graphCreation.whichWay(graph[curPos[0]][curPos[1]])        # Sets the value of rowIncrement and colIncrement
        row, col = curPos[0], curPos[1]                                                                     # Sets the value of row and col
        tempGraph[row][col] = 1 if backwardsCost == False else cost                                                                             # Sets the value of tempGraph[row][col]
        counter = 0                                                                                         # Sets the value of counter
        #print("Looking for arrow color: ", arrowLooky)
        while (row >= 0 and row < len(graph)) and (col < len(graph[0]) and col >= 0):                       # While Loop
            exploredPath = path + f" {counter}{arrowLooky[1]}"                                              # Adds to exploredPath

            if graph[row][col] == "O":                                                                      # Found the goal
                #print(path + f" {counter}{arrowLooky[1]}")                                                  # Debug print statement
                return exploredPath                                                                         # Returns the path to the user
            
            elif graph[row][col][0] == arrowLooky[0] and ((backwardsCost == False and tempGraph[row][col] == 0)
                 or (backwardsCost == True and computePathCost(exploredPath) < tempGraph[row][col])):       # unexplored node
                
                tempGraph[row][col] = computePathCost(exploredPath) if backwardsCost == True else 0         # Sets the value of tempGraph[row][col]
                
                newPos = (row, col)                                                                         # Sets the value of newPos
                
                pqueueCost = 0                                                                              # Sets the value of pqueueCost
                if userHeuristic == True:                                                                   # Looking at heurisitic values
                    pqueueCost += manhattanHeuristic(newPos, endingCoor)                                    # Adds to the value of pqueueCost
                
                if backwardsCost == True:                                                                   # If we are looking at the backwards past cost
                    pqueueCost += computePathCost(exploredPath)                                             # Adds to the value of pqueueCost
                    
                pqueue.append([newPos, exploredPath, pqueueCost])                                           # Appends to pqueue

            row += rowIncrement                                                                             # Adds to the value of row
            col += colIncrement                                                                             # Adds to the value of col
            counter += 1                                                                                    # Adds to the value of counter
   
        pqueue.sort(key = obtainPathCost)                                                                   # Sorts the pqueue
        
        

# This is the method that will be used to help sort the list. It will return the value of the last index in the list that is passed
def obtainPathCost(elem):                                                                                   # Method Block
    return elem[-1]                                                                                         # Returns the cost to the user



# This is the method that will be used to determine what the backwards path cost is for a given path that 
# is passed to the user. Basically it will look at the steps used to take a path up to the point it is passed
# into the caller function and will return an integer for the number of steps taken.
def computePathCost(path):                                                                                  # Method Block
    
                                                                                                            # VARIABLE DEFINITIONS
    cost = 0                                                                                                # Defines cost
    intermediary = 0                                                                                        # Sets the value of intermediary
    
    separatedList = path.split(" ")                                                                         # Separates the directions
    
    for singularStep in separatedList:                                                                      # For Loop
        
        if len(singularStep) < 2:                                                                           # Should only ever occur for the first step in the list
            continue                                                                                        # Continues to next iteration of loop
        intermediary = 0                                                                                    # Sets the default value of intermediary
        for LCV in range(len(singularStep)):                                                                # Nested Loop
            
            match singularStep[LCV]:                                                                        # MAtch case
                case "N" | "S" | "W" | "E":                                                                 # Found a cardinal direction
                    #print("Found at index:", LCV, "for", singularStep)                                      # Debug print statement
                    break                                                                                   # Breaks out of the nested loop
                case _:                                                                                     # Still looking at integers
                    intermediary += 1                                                                       # Adds to the value of intermediary
        
        cost += int(singularStep[: intermediary])                                                           # Adds to the value of cost
        
    return cost                                                                                             # Returns the value of cost to the user
        


# This will be used as a staging area to run the traversal algorithms from
def main():                                                                                                 # Main Block

    args = graphCreation.sys.argv                                                                           # Gets the arguments entered into the terminal
    
    if len(args) < 3:                                                                                       # Too few arguments entered
        raise Exception("Too few arguments entered. Must be entered either of the following ways:\n\t\'python graphTraversal.py {dimension1} {dimension2} {traversalMethod}\' \n\t\'python graphTraversal.py {dimension1} {traversalMethod}\'")
    elif len(args) > 4:
        raise Exception("Too many arguments entered. Must be entered either of the following ways:\n\t\'python graphTraversal.py {dimension1} {dimension2} {traversalMethod}\' \n\t\'python graphTraversal.py {dimension1} {traversalMethod}\'")
    
    
    doTraversal(args[1:])                                                                               # Call to method doTraversal

    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error! {e}")
    
    finally:
        print("The program is now done")