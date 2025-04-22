# Jason Rudinsky
# April 22, 2025
# Autonomous Mobile Robots - Grad project

# This is the code that will be used to traverse through a given graph using the various search methods,
# and the program will output the path taken from the start position to the end position of the various graphs to a file.
# The program will in a separate file also output the time it took to traverse said graph to the user as well.

# 4/22/2025 - Original Version

import graphCreation, heapq                                                                                 # Importing the various modules
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
    else:                                                                                                   # Two dimensions to look at
        row, col, traversalMethod = int(arguments[0]), int(arguments[1]), arguments[-1].upper()             # Sets the values of row, col, and traversalMethod
            
    
    print(f"Looking for directory: Graphs/{row} by {col}")
    print(traversalMethod)


# This will be used as a staging area to run the traversal algorithms from
def main():                                                                                                 # Main Block

    args = graphCreation.sys.argv                                                                           # Gets the arguments entered into the terminal
    
    if len(args) < 3:                                                                                       # Too few arguments entered
        raise Exception("Too few arguments entered. Must be entered either of the following ways:\n\t\'python graphTraversal.py {dimension1} {dimension2} {traversalMethod}\' \n\t\'python graphTraversal.py {dimension1} {traversalMethod}\'")
    elif len(args) == 3:                                                                                    # It's a square
        
        match args[-1].upper():                                                                             # Looking at the traversal method
            case "DFS":                                                                                     # Doing DFS traversal
                print("We will perform a DFS Search")                                                       # Debug print statement
                
            case _:                                                                                         # Unknown search method entered
                raise Exception(f"{args[-1]} is not a recognized search method. The traversals that can be done are \'DFS\', \'BFS\', \'A*\', \'UCS\', or \'GREEDY\'")        
            
    elif len(args) == 4:
        print("Differing dimensions perhaps")                                                               # Debug print statement
        
        match args[-1].upper():                                                                             # Looking at the traversal method
            case "DFS":                                                                                     # Doing DFS traversal
                print("We will perform a DFS Search")                                                       # Debug print statement
                
            case _:                                                                                         # Unknown search method entered
                raise Exception(f"{args[-1]} is not a recognized search method. The traversals that can be done are \'DFS\', \'BFS\', \'A*\', \'UCS\', or \'GREEDY\'")
           
    else:
        raise Exception("Too many arguments entered. Must be entered either of the following ways:\n\t\'python graphTraversal.py {dimension1} {dimension2} {traversalMethod}\' \n\t\'python graphTraversal.py {dimension1} {traversalMethod}\'")
    
    
    doTraversal(args[1:])                                                                               # Call to method doTraversal

    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error! {e}")
    
    finally:
        print("The program is now done")