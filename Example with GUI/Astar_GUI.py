from pickle import NONE
import shlex
import re
from tkinter import Tk
import tkinter
from pyamaze import maze,COLOR,agent, textLabel
#from pyamaze import maze,agent,textLabel
from queue import PriorityQueue
from aStarDemo import aStar
import _tkinter

class Micromouse:
    def __init__(self, ifile, origPos =(1,1), size = 4, draw=False):
        self.ifile = ifile
        self.size = size
        self.csvfile='tmp.csv'
        self.origPos=origPos
        self.draw = draw # YOU MAY NEED TO PASS draw into the maze object below
        self.maze = maze(rows=self.size, cols=self.size, draw = draw)
        self.dict ={}
        # read the input file and get tokenizer for dictionary list
        self.processInput(ifile)
        self.parsefunc(ifile)
        # process the dictionary list and sort the dictionary list
        # before write the list into a cvs file (self.csvfile)
        self.processDict()
       

    # this function will take an input line and parse into 5 fields
    # field 1: cell., field 2: north distance...
    def parsefunc(self, line):
        line = line.replace(",", ", ")
        output = shlex.split(line)
        output = [re.sub(r",$","",w) for w in output]
        return output


    # this function will take an input file and get each line
    # and pass each line to parse the line for 5 fields
    # then add them into the dictionary
    def processInput(self,ifile):
        file1 = open(self.ifile, 'r')
        Lines = file1.readlines()
        count = 0
       
        #Strips the newline character
        #for each line in the input file, format and strip the data
        for line in Lines:
            count += 1
            output = self.parsefunc(line.strip())
           
            #this for loop will change the lidar data values into either
            #0s or 1s based on the value being greater than or less than 0.25
            for indx in range(1,5):
                if float(output[indx]) > 0.25:
                    output[indx] =1
                else:
                    output[indx] =0
                   
            #this is the most important line in the function, the first value of the input file
            #or the coordinates are stripped of spaces and placed as the key of the dictionary
            #while the four following values (N,E,S,W) are placed as the value of the dictionary
            self.dict[str(output[0]).replace('  ',' ')] = str(tuple(output[1:5])).replace(' ','')
           
            #this section ensures the variable type of the dictionary
            #is both an int for the dictionary value and tuple for the
            #coordinate value
            self.dict[(output[0])]=tuple(output[0])
            for indx1 in range(1,5):
                output[indx1] = int(output[indx1])
           

    # the dictionary is completed after reading each file
    # we can write back the dictionary into a csv file base on the order
    # of each cell
    def processDict(self):
        #open the csv file and write to it
        #first write the cell and EWNS header
        with open(self.csvfile,'w') as csv_file:
            csv_file.write("  cell  ,E,W,N,S")
            csv_file.write("\n")
           
            #for j and i of 1 to 4, the strtoken will search for
            #coordinates in the organization of (j,i) in the dictionary
            for j in range (1,5):
                for i in range (1,5):
                    strtoken = '({}, {})'.format(i,j)
                   
                    #if that coordinate is found as a key in the dictionary, the value is the following
                    #four values for EWNS. This formating removes any parentheses for the value pair.
                    if strtoken in self.dict:
                        csv_file.write('"{}",{}'.format(strtoken,str(self.dict[strtoken])[1:-1]))
                        csv_file.write("\n")
                       
                    #if the coordinate is not listed as a key in the dictionary, the the value is 0000
                    else:
                        csv_file.write('"{}",{}'.format(strtoken,"0,0,0,0"))
                        csv_file.write("\n")
                   
       
    def createMaze(self):
        # maze created based the self.csvfile
        self.maze.CreateMaze(x=self.origPos[0], y=self.origPos[1], loopPercent=100, loadMaze=self.csvfile)
        # displace the maze based the created maze
       #  self.maze.run()
   
    #function designed to take function aStar from aStardemo.py to find the shortest path
    def findPath(self,  dst):
       self.maze._goal=dst
       searchPath,aPath,fwdPath=aStar(self.maze) # passing the goal cell through the maze path algorithms

       return fwdPath # returning the shortest path to goal cell
 
if __name__=="__main__":
    # add a
    a = Micromouse('inputfile1.txt', (2,2), size = 4, draw=True)
    a.createMaze()

    print ()
    print ("GENERATED MAZE MAP IS SHOWN BELOW:")
    print ()
    print ("***Shortest path is calculated sifting through this pyamaze generated dictionary***")
    print ()
    #print (a.maze.maze_map)
   
    # create a function for findPath
    fwdPath=a.findPath((2,2)) # this coordinate represents the goal cell
    # coordinate may be changed to whatever pleased
    # be sure to change the coordinate in line 116 to the same coordinate as line 127


    print ()
    print ("SHORTEST PATH TO GOAL FOR INPUT START & FINISH IS BELOW:")
    print ()
    print ("***Formatting of path is: {(previous cell): (current cell)}**")
    print ("***Start location is the last key and value of the dictionary, goal is the first**")
    print ("***Path must be read from right to left**")
    print ()
    print ("PATH: ", fwdPath)
    print ()
   
   #creating the agent to follow the found path
    m=a.maze # setting m = maze(dimension size)
    c=agent(m,footprints=True,color=COLOR.red)
    m.tracePath({c:fwdPath},delay=300)
    l=textLabel(m,'A Star Path Length',len(fwdPath)+1)
    m.run()
