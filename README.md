The repository will house 3 programs:
  1) The First Program:
        - A program that will create a 2-d representation of a graph using the directions (N, NE, NW, E, SE, S, SW, W) and the colors of red and blue.
        - This program will also make it so the program will either make both graphs that have the ability to be navigated to a terminal point, and graphs that can be made with no way to reach their endpoint.

  2) The Second Program:
        - A program that will when given a file, will run the different graph traversal algorithms (BFS, DFS, UCS, Greedy, and A*) and store the results (How long it took to compute the path, or lack thereof) for each graph
  
  3) The Third Program:
       - A Program that will make sure that the path that was computed in the previous program leads to the correct terminal position

The first program now makes only valid graphs, and checks in the program to make sure that the graphs created have at least one possible path that leads to the terminal state. The second program will use search algorithms to traverse the graphs and will store the paths in one file, and the time it took to traverse the graphs in another.

To create graphs and store them just use:
  
``` python graphCreation.py {row length} {column length} {number of graphs} ```
