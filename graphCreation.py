# Jason Rudinsky
# April 18, 2025
# Autonomous Mobile Robots - Grad project

# This is the code that will be used to create the graphs I need to traverse through for my little presentation. 
# It will make sure that the graphs are able to reach the desired target by performing a DFS search once a graph is created.

# 4/18/2025 - Original Version
# 4/22/2025 - Added the methods needed to make a maze of user designated size, as well as the method to traverse the created
    # maze and return a path. I also made the necessary methods to traverse the maze via the given path and return whether or 
    # not the path is valid. Also added the code to successfully write the maze and it's dimensions to a file.
# 4/22/2025 @ 2:28 pm - Removed the option to go SE on the starting position due to the fact that it could theoretically get
    # to the goal position without having to take any other directional turns
# 4/22/2025 @ 3:00 pm - Altered the DFSTraversal method into a more uniform and abstract method so that I can call the method to
    # perform both BFS and DFS traversal when I want to.
# 4/23/2025 - Imported the graphTraversal program to run the check to make sure a graph is able to reach it's end goal using a 
    # greedy approach instead of the previous DFS approach that I was using to make it on average just a little bit faster to 
    # double check that the graph that was created is valid.



import os, sys, random
import graphTraversal



# This is the method that will be used to create graphs that will be used. 
# The graphs will be created using a 2d list and then the results will be passed to a created file.
# Before the graphs are passed to a file, we will first make sure that the created graph has a path 
# that when starting from the top left corner, we can make it to the bottom right hand corner which is the terminal position.
def createGraphs(rows, columns, numGraphs = 1):                                                             # Method Block

                                                                                                            # VARIABLE DEFINITIONS
    rows = int(rows)                                                                                        # Integer casting
    columns = int(columns)                                                                                  # integer casting
    numGraphs = int(numGraphs)                                                                              # Integer casting
    graph = [["" for j in range(columns)] for i in range(rows)]                                             # Shorthand for creating the list

    directions = ["N", "E", "S", "W", "NE", "NW", "SE", "SW"]                                               # Defines the cardinal directions 
    arrows = ["R", "B"]                                                                                     # Defines the arrow colors
    #printList(graph)
    #print(numGraphs)

    correctlyMade = 0                                                                                       # Defines an integer for the number of correctly made graphs with a reachable end
    #print("Hi:", graph[len(graph) - 1][len(graph[0]) - 1])
    
    if not os.path.exists("Graphs"):                                                                        # If the path does not exists
        os.mkdir("Graphs")                                                                                  # Makes the folder

    if not os.path.exists(f"Graphs/{rows} by {columns}"):                                                   # If the folder does not exist
        os.mkdir(f"Graphs/{rows} by {columns}")                                                             # Make the folder
        incremental = 0                                                                                     # Sets the value of incremental
    else:                                                                                                   # The folder already exists
        folderLooky = os.listdir(f"Graphs/{rows} by {columns}")                                             # Looks for the directory and obtains all files in it
        
        incremental = 0                                                                                     # Sets the value of incremental
        if len(folderLooky) > 0:                                                                            # If the folder is non-empty
            folderLooky = list(filter(lambda x: "graph" in x, folderLooky))                                 # Seeks to filter out any unwanted txt files
            folderLooky.sort(key = findNumeric)                                                             # Sorts the items in folderLooky

            file = folderLooky[-1]                                                                          # Sets the value of file
            file = file[file.find("h") + 1: file.find(".")]                                                 # String slicing file to find the numeric value

            incremental = int(file) + 1                                                                     # Updates the value of incremental

    while correctlyMade < numGraphs:                                                                        # While Loop

        graph = fillTheGraph(graph, directions, arrows)                                                     # Call to method fillTheGraph
        if isValidGraph(graph):                                                                             # Calls to method isValidGraph
            #print("Valid Graph detected:")
            #printList(graph)
            myFile = open(f"Graphs/{rows} by {columns}/graph{incremental}.txt", "w")                        # OPens the new file
    
            myFile.write(f"{rows} {columns}\n")                                                             # Writes the dimensions of the graph

            for i in graph:                                                                                 # For Loop
                myFile.write(" ".join(i))                                                                   # Writes the information to the file
                myFile.write("\n")                                                                          # Writes a newline character to the file
            else:                                                                                           # The loop is done
                myFile.close()                                                                              # Closes the file

            incremental += 1                                                                                # Adds to the value of incremental
            correctlyMade += 1                                                                              # Adds to the value of correctlyMade



# This is the method that will be used to return a number that is in the graph#.txt name
def findNumeric(txtFile):                                                                                   # Method BLock
    
    return int(txtFile[txtFile.find("h") + 1: txtFile.find(".")])                                           # Returns an integer to the user


# This is the method that will be used to create a graph that could potentially have a valid path to a goal,
# it will randomly fill in the directions to take from the directions and arrow fields that were passed in an 
# the program will return a filled in graph to the user
def fillTheGraph(graph, directions, arrows):                                                                # Method Block
    
    for rowIndex in range(len(graph)):                                                                      # For Loop
        for colIndex in range(len(graph[0])):                                                               # Nested loop
            
            if rowIndex == 0 and colIndex == 0:                                                             # Limiting the number of values for the first item in the array
                temp = f'{random.choice(arrows)}-{random.choice(["E", "S"])}'                               # Defines a temp value
            else:
                temp = f"{random.choice(arrows)}-{random.choice(directions)}"                               # Defines a temp value
            
            graph[rowIndex][colIndex] = temp                                                                # Sets the value of graph[rowIndex][colIndex]
    else:
        
        graph[len(graph) - 1][len(graph[0]) - 1] = "O"                                                      # Updates the bottom righthand element in the 2d list
        
        return graph                                                                                        # Returns the graph to the user



# This is the method that will be used to determine if the graph that is passed in
# can properly be navigated to its exit, i.e., the O in the bottom right hand corner of the map.
def isValidGraph(graph):                                                                                    # Method Block
    path = graphTraversal.greedy(graph, True, True)                                                         # Returns the path to the user

    if path != None:

        row, col = 0, 0                                                                                     # Sets the value of row and col
        
        for direction in path.split(" ")[1: ]:                                                              # For Loop
            rowIncrement, colIncrement, arrowLooky = whichWay(graph[row][col])                              # Call to method whichWay
            multiple, theDirection = determineDirection(direction)                                          # Call to method determineDirection

            #print(f"Looking ({row}, {col}) and will take {multiple} steps {theDirection}, {arrowLooky}")    # Debug print statement

            if arrowLooky[1] != theDirection:                                                               # If we went the wrong way
                print(f"Improper direction attempted in cell ({row}, {col})")                               # Prints out to the user
                return False                                                                                # Returns false to the user

            row += (rowIncrement * multiple)                                                                # Adds to the value of row
            col += (colIncrement * multiple)                                                                # Adds to the value of col
            
            if row < 0 or row >= len(graph):                                                                # Out of graph bounds
                print("Out of bounds in the row direction")                                                 # Prints out to the user
                return False                                                                                # Returns false to the user
            elif col < 0 or col > len(graph[0]):                                                            # Out of graph bounds
                print("out of bounds in the column direction")                                              # Prints out to the user
                return False                                                                                # returns false to the user
            #print(f"Now Looking ({row}, {col}) and will check the color of the arrow (Should be {arrowLooky[0]})")
            
            if graph[row][col] == "O":                                                                      # Reached the terminal spot
                return True                                                                                 # REturns true to the user

            if graph[row][col][0] != arrowLooky[0]:                                                         # Looking at the improper arrow color
                print("Stopped at the wrong arrow")                                                         # Prints out to the user
                return False                                                                                # Returns false to the user
        else:
            #print(f"Value in ({row}, {col}) is: {graph[row][col]}")
            return True                                                                                     # Returns true to the user
    
    return False                                                                                            # Returns false to the user



# This is the method that will attempt to traverse the graph via a DFS graph traversal. 
# If a path can be found then the string of the path will be returned to the user. 
# Otherwise the latest path that was attempted will be returned.
def traversal(graph, depth):                                                                                # Method Block

                                                                                                            # VARIABLE DEFINITIONS
    rowIncrement, colIncrement = 0, 0                                                                       # Defines values for the row and column increments
    row, col = 0, 0                                                                                         # Defines values for the current values of row and col
    steps = 0                                                                                               # Defines a value for the number of steps taken
    path, arrowLooky = "", ""                                                                               # Defines a value for the path and arrowLooky
    queue = []                                                                                              # Data Structure to store the DFS traversal of the stack
    dfsGraph = [["" for j in range(len(graph[0]))] for i in range(len(graph))]                              # Shorthand for creating the list

    startingPosition = [(0, 0), ""]                                                                         # Defines the startingPosition
    queue.append(startingPosition)                                                                          # Appends the starting position to the user
    #printList(graph)
    
    while len(queue) != 0:                                                                                  # As long as we have coordinates to traverse
        
        if depth == True:                                                                                   # If we are doing DFS
            curPos, path = queue.pop()                                                                      # Pops from the rear of the stack
        else:
            curPos, path = queue.pop(0)                                                                     # Pops from the front of the queue
        
        #print(curPos, path)
        
        rowIncrement, colIncrement, arrowLooky = whichWay(graph[curPos[0]][curPos[1]])                      # Sets the value of rowIncrement and colIncrement
        row, col = curPos[0], curPos[1]                                                                     # Sets the value of row and col
        dfsGraph[row][col] = "explored"                                                                     # setting the value of graph[row][col]
        counter = 0                                                                                         # Sets the value of counter
        #print("Looking for arrow color: ", arrowLooky)
        while (row >= 0 and row < len(graph)) and (col < len(graph[0]) and col >= 0):                       # While Loop
            
            if graph[row][col] == "O":                                                                      # Found the goal
                #print("Found")
                #print(path + f" {counter}{arrowLooky[1]}")                                                  # Debug print statement
                return path + f" {counter}{arrowLooky[1]}"                                                  # Returns the path to the user
            elif graph[row][col][0] == arrowLooky[0] and dfsGraph[row][col] == "":                          # unexplored node
                exploredPath = path + f" {counter}{arrowLooky[1]}"                                          # Adds to exploredPath
                dfsGraph[row][col] = "visited"                                                              # Sets the value of graph[row][col]

                newPos = (row, col)                                                                         # Sets the value of newPos
                queue.append((newPos, exploredPath))

            row += rowIncrement                                                                             # Adds to the value of row
            col += colIncrement                                                                             # Adds to the value of col
            counter += 1                                                                                    # Adds to the value of counter
           


# This is the method that will be used to determine which way in which 
# the program will be looking to traverse towards. The program will return 
# both the arrow color at the current position as well as the increments of both the row and column
def whichWay(directions):                                                                                   # Method Block

                                                                                                            # VARIABLE DEFINITIONS
    separation = directions.split("-")                                                                      # Sets the value of separation
    row, col = 0, 0                                                                                         # Sets the value of row and col

    for direction in separation[1]:                                                                         # For Loop

        if direction == "S":                                                                                # If we are going south
            row += 1                                                                                        # Adds from the value of row
        elif direction == "E":                                                                              # If we are going east
            col += 1                                                                                        # Adds to the value of col
        elif direction == "W":                                                                              # If we are going west
            col -= 1                                                                                        # Subtracts from the value of col
        else:                                                                                               # We are going north
            row -= 1                                                                                        # Subtracts from the value of row

    if separation[0] == "R":                                                                                # If we are looking at a red arrow
        separation[0] = "B"                                                                                 # Sets the value of separation[0]
    else:                                                                                                   # Looking at a blue arrow
        separation[0] = "R"                                                                                 # Sets the value of separation[0]
        
    return row, col, separation                                                                             # Returns the values to the user



# This is the method that will be used to determine the direction that the path wants us to take 
# as well as the number of steps in that direction to take
def determineDirection(theDirection):                                                                       # Method Block

                                                                                                            # VARIABLE DEFINITIONS
    index = 0                                                                                               # Sets the value of index

    while index < len(theDirection):                                                                        # While Loop

        match theDirection[index]:                                                                          # Match case
            case "N" | "W" | "E" | "S":                                                                     # Found the first instance of the cardinal directions
                break                                                                                       # Breaks out of the while loop
            case _:
                index += 1                                                                                  # Adds to the value of index

    return int(theDirection[: index]), theDirection[index: ]                                                # Returns the information to the user



# This is just a helper method that will be used so that I can see the information in the graph. 
# It's just a basic method to print a 2d list
def printList(graph):                                                                                       # Method Block

    for row in graph:                                                                                       # For Loop
        for col in row:                                                                                     # Nested For Loop
            temp = str(col)
            print(f"{temp:^5s}", end = " ")                                                                  # Prints out to the user
        print("")                                                                                           # Prints a new line character





def main():                                                                                                 # Main Block

    args = sys.argv                                                                                         # Gets all the system arguments

    if len(args) < 3:                                                                                       # If the dimensions for a graph were not entered
        raise Exception("Error! Expected at least 3 arguments. The program accepts the following forms of input: \n\t\'python graphCreation.py {row dimension} {column dimension}\' \
                        \n\t\'python graphCreation.py {row dimension} {column dimension} {number of graphs to create}\'")                                            
                                                                                                            # Raises an exception to the user
    
    args = args[1:]                                                                                         # Updates the value of args

    if len(args) == 2:                                                                                      # Only the dimensions of the graph were entered
        createGraphs(args[0], args[1])                                                                      # Call to method createGraphs
    elif len(args) == 3:                                                                                    # Dimensions + number of graphs were entered
        createGraphs(args[0], args[1], args[2])                                                             # Call to method createGraphs
    else:
        raise Exception("Error! Expected at most 3 arguments. The program accepts the following forms of input: \n\t\'python graphCreation.py {row dimension} {column dimension}\' \
                        \n\t\'python graphCreation.py {row dimension} {column dimension} {number of graphs to create}\'")                                            
                                                                                                            # Raises an exception to the user
    
    
if __name__ == "__main__":                                                                                  # If this is the main program being used
    try:
        main()                                                                                              # Calls the main method
    except Exception as e:
        print(f"Error! {e}")
    finally:
        print("Program is done. Goodbye!")        