# Jason Rudinsky
# April 18, 2025
# Autonomous Mobile Robots - Grad project

# This is the code that will be used to create the graphs I need to traverse through for my little presentation. 
# It will make sure that the graphs are able to reach the desired target by performing a DFS search once a graph is created.

# 4/18/2025 - Original Version


import sys, random



# This is the method that will be used to create graphs that will be used. 
# The graphs will be created using a 2d list and then the results will be passed to a created file.
# Before the graphs are passed to a file, we will first make sure that the created graph has a path 
# that when starting from the top left corner, we can make it to the bottom right hand corner which is the terminal position.
def createGraphs(rows, columns, numGraphs = 1):                                                             # Method Block

                                                                                                            # VARIABLE DEFINITIONS
    rows = int(rows)                                                                                        # Integer casting
    columns = int(columns)                                                                                  # integer casting
    graph = [["" for j in range(columns)] for i in range(rows)]                                             # Shorthand for creating the list

    directions = ["N", "E", "S", "W", "NE", "NW", "SE", "SW"]                                               # Defines the cardinal directions 
    arrows = ["R", "B"]                                                                                     # Defines the arrow colors
    printList(graph)


    correctlyMade = 0                                                                                       # Defines an integer for the number of correctly made graphs with a reachable end
    #print("Hi:", graph[len(graph) - 1][len(graph[0]) - 1])
    while correctlyMade < numGraphs:                                                                        # While Loop

        graph = fillTheGraph(graph, directions, arrows)                                                     # Call to method fillTheGraph
        printList(graph)
        if isValidGraph(graph):                                                                             # Calls to method isValidGraph
            print("Valid Graph detected:")
            printList(graph)
            correctlyMade += 1                                                                                  # Adds to the value of correctlyMade

        break


# This is the method that will be used to create a graph that could potentially have a valid path to a goal,
# it will randomly fill in the directions to take from the directions and arrow fields that were passed in an 
# the program will return a filled in graph to the user
def fillTheGraph(graph, directions, arrows):                                                                # Method Block
    
    for rowIndex in range(len(graph)):                                                                      # For Loop
        for colIndex in range(len(graph[0])):                                                               # Nested loop
            
            if rowIndex == 0 and colIndex == 0:                                                             # Limiting the number of values for the first item in the array
                temp = f"{random.choice(arrows)}-{random.choice(["E", "S", "SE"])}"                         # Defines a temp value
            else:
                temp = f"{random.choice(arrows)}-{random.choice(directions)}"                               # Defines a temp value
            
            graph[rowIndex][colIndex] = temp
    else:
        
        graph[len(graph) - 1][len(graph[0]) - 1] = "O"                                                      # Updates the bottom righthand element in the 2d list
        
        return graph                                                                                        # Returns the graph to the user



# This is the method that will be used to determine if the graph that is passed in
# can properly be navigated to its exit, i.e., the O in the bottom right hand corner of the map.
def isValidGraph(graph):                                                                                    # Method Block
    DFSTraversal(graph)
    return False


# This is the method that will attempt to traverse the graph via a DFS graph traversal. 
# If a path can be found then the string of the path will be returned to the user. 
# Otherwise the latest path that was attempted will be returned.
def DFSTraversal(graph):                                                                                    # Method Block

                                                                                                            # VARIABLE DEFINITIONS
    rowIncrement, colIncrement = 0, 0                                                                       # Defines values for the row and column increments
    row, col = 0, 0                                                                                         # Defines values for the current values of row and col
    steps = 0                                                                                               # Defines a value for the number of steps taken
    path, arrowLooky = "", ""                                                                               # Defines a value for the path and arrowLooky
    queue = []                                                                                              # Data Structure to store the DFS traversal of the stack
    dfsGraph = [["" for j in range(len(graph[0]))] for i in range(len(graph))]                              # Shorthand for creating the list

    startingPosition = [(0, 0), ""]
    queue.append(startingPosition)

    while len(queue) != 0:
        curPos, path = queue.pop()

        print(curPos, path)

# This is just a helper method that will be used so that I can see the information in the graph. 
# It's just a basic method to print a 2d list
def printList(graph):                                                                                       # Method Block

    for row in graph:                                                                                       # For Loop
        for col in row:                                                                                     # Nested For Loop
            print(f"{col:^5s}", end = " ")                                                                   # Prints out to the user
        print("")                                                                                           # Prints a new line character
    print("\n\n")

def main():                                                                                                 # Main Block

    args = sys.argv

    print(args)

    if len(args) < 3:
        raise Exception("Error! Expected at least 3 arguments.")
    args = args[1:]
    createGraphs(args[0], args[1])


main()