#!/usr/bin/python
from A_star import Micromouse

#### THIS SCRIPT IS SOLELY FOR EXECUTION PURPOSES, THE MICROMOUSE CLASS FUNCTIONS AND FINDPATH ALGORITHM IS
#### FOUND IN THE OTHER FILE A_STAR.PY AND THE GENERATED MAZE_MAP IN PYAMAZE.PY

if __name__=="__main__":
    
    #size of the maze can be set using the size variable with matching dimensional input file
    #the second variable in this class call is the starting DISPLAY location of the maze
    # it doesn't affect the A_star algorithm to determine path from start to finish
    a = Micromouse('inputfile.txt', (2,3), size = 4, draw=True)
    a.createMaze()

    #these statements will simply print the maze_map of the generated maze from your input file
    print ()
    print ("GENERATED MAZE MAP IS SHOWN BELOW:")
    print ()
    print ("***Shortest path is calculated sifting through this pyamaze generated dictionary***")
    print ()
    print (a.maze.maze_map)
    
    
    # this function calls the findPath for the start and goal
    # in this example start is (2,3) and goal is (4,4), but you can 
    # adjust to any cells in the 4x4 maze 
    fwdPath=a.findPath((2,3), (4,4))


    #these statements will simply print the desired output you are looking for
    print ()
    print ("SHORTEST PATH TO GOAL FOR INPUT START & FINISH IS BELOW:")
    print ()
    print ("***Formatting of path is: {(previous cell): (current cell)}***")
    print ("***Start location is the last key and value of the dictionary, goal is the first***")
    print ("***Path must be read from right to left**")
    print ()
    print ("PATH: ", fwdPath)
    print ()
    


