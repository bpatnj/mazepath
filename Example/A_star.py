from pickle import NONE
import shlex
import re
from pyamaze import maze,COLOR,agent, textLabel
#from pyamaze import maze,agent,textLabel
from queue import PriorityQueue

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
        self.maze.run()
    
    #heuristic score function
    #calculate manhattan distance for the cell input arguments
    def h(self, cell1,cell2):
        
        #x1,y1 and y1,y2 is cell1,cell2 and the abs subtraction is the 
        #horizontal and vertical distance not including walls from the two locations
        x1,y1=cell1
        x2,y2=cell2
        return abs(x1-x2) + abs(y1-y2)


    #findPath will calculate the best path from start to goal based on the
    #maze structure
    def findPath(a, start, goal):
        
        #set start to input variable start
        start == (start)
        
        #set goal to input variable goal
        goal == (goal)
        
        #f_score  = g_score + h_score
        #set g_score of all cells to infinity for the generated maze grid
        g_score={cell:float('inf') for cell in a.maze.grid}
        g_score[start]=0
        
        #set f_score of all cells to infinity for the generated maze grid
        #f_score is calculated by comparing the manhattan distance goal per cell
        #and adding it to the g_score 
        f_score={cell:float('inf') for cell in a.maze.grid}
        f_score[start]=a.h(start,goal)

        #imported function priority queue that allows for tuples to be stored
        open=PriorityQueue()
        
        #store the f_score, h_score, and start coordinates to the goal
        #f_score of starting location is just h_score, g_score is 0 until a step is made
        open.put((a.h(start,goal),a.h(start,goal),start))
        aPath={}
        searchPath=[start]
        
        #while loop which reads values of priority queue
        while not open.empty():
            currCell=open.get()[2]
            
            #if the currCell pulled from the priority queue is equal to the goal
            #input argument, break the while loop, otherwise explore the maze_map
            #from pyamaze
            if currCell==goal:
                break
            
            #for the key value ESNW in the generated maze_map from pyamaze
            #carry out the following if statements
            for d in 'ESNW':
                
                #the maze_map 
                if a.maze.maze_map[currCell][d]==True:
                    
                    #if the coordinate read is E and the value for it is 1 or open wall
                    # add 1 to currCell[1]
                    if d=='E':
                        childCell=(currCell[0],currCell[1]+1)
                        
                    #if the coordinate read is W and the value for it is 1 or open wall
                    # subtract 1 from currCell[1]
                    if d=='W':
                        childCell=(currCell[0],currCell[1]-1)    
                        
                    #if the coordinate read is N and the value for it is 1 or open wall 
                    # subtract 1 from currCell[0]
                    if d=='N':
                        childCell=(currCell[0]-1,currCell[1])
                        
                    #if the coordinate read is S and the value for it is 1 or open wall 
                    # add 1 to currCell[0]
                    if d=='S':
                        childCell=(currCell[0]+1,currCell[1])

                    #variable temp_g_score is increased by 1 for each step
                    temp_g_score=g_score[currCell]+1
                    
                    #variable temp_f_score is calculated by adding g_score to the h_score
                    #with arguments, start and the childCell. Essentially a new f_score for a childCell calculated
                    # by if statements from above 
                    temp_f_score=temp_g_score+a.h(childCell,start)

                    #if temp_f_score < f_score of the child cell then..
                    if temp_f_score < f_score[childCell]:
                        
                        #then make the g_score of the child cell equal to temp_g_score
                        g_score[childCell]= temp_g_score
                        
                        #and also make the f_score of the childCell to the temp_f_score
                        f_score[childCell]= temp_f_score
                        
                        #place the calculated temp_f_score, h_score of the child cell and location
                        #into the priority queue "open"
                        open.put((temp_f_score,a.h(childCell,start),childCell))

                        #dictionary aPath which is initialized above has the key of the child cell
                        #and value of the curr Cell. This key value pair is the main output of the A*star routine
                        aPath[childCell]=currCell
                  
                  
        #new dictionary is created fwdPath      
        fwdPath={}
        cell=goal
        
        #while the cell isnt the destination goal
        while cell!=start:
            
            #the key of the dictionary is aPath[cell] while the 
            #value is cell
            fwdPath[aPath[cell]]=cell
            cell=aPath[cell]
            
        #output of this function is fwdPath which is called
        #in the main function
        return fwdPath

    
if __name__=="__main__":
    
    a = Micromouse('inputfile.txt', (2,3), size = 4, draw=True)
    a.createMaze()

    print ()
    print ("GENERATED MAZE MAP IS SHOWN BELOW:")
    print ()
    print ("***Shortest path is calculated sifting through this pyamaze generated dictionary***")
    print ()
    print (a.maze.maze_map)
    
    # create a function for findPath
    fwdPath=a.findPath((2,3), (4,4))
    #f=agent(a.maze,footprints=False)
    #f.tracePath({a:fwdPath})
    #l=textLabel(m,'A Star Path Length',len(fwdPath)+1)

    #m.run()

    print ()
    print ("SHORTEST PATH TO GOAL FOR INPUT START & FINISH IS BELOW:")
    print ()
    print ("***Formatting of path is: {(previous cell): (current cell)}***")
    print ("***Start location is the last key and value of the dictionary, goal is the first***")
    print ("***Path must be read from right to left***")
    print ()
    print ("PATH: ", fwdPath)
    print ()
     
    # a=agent(a.maze,footprints=True)
    # m.tracePath({a:fwdPath})
    # l=textLabel(m,'A Star Path Length',len(fwdPath)+1)