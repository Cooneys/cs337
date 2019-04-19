import sys
import os


######################################
## Class: State
## input: list river
######################################

class State():
    def __init__(self, river):
        leftBank = river[0].split(",")
        rightBank = river[1].split(",")
        self.lbChickens = leftBank[0]
        self.lbWolves = leftBank[1]
        self.lbBoat = leftBank[2]
        self.rbChickens = rightBank[0]
        self.rbWolves = rightBank[1]
        self.rbBoat = rightBank[2]

    def printState(self):
        print("Left Bank: %s chickens, %s wolves, %s boat"%(self.lbChickens, self.lbWolves, self.lbBoat), end=" - ")
        print("Right Bank: %s chickens, %s wolves, %s boat"%(self.rbChickens, self.rbWolves, self.rbBoat))



######################################
## Mode: bfs
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runBfs(startRiver, goalRiver):
    initial = State(startRiver)
    initial.printState()
 

######################################
## Mode: dfs
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runDBfs(startRiver, goalRiver):
   return 


######################################
## Mode: iddfs
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runIddfs(startRiver, goalRiver):
   return 


######################################
## Mode: astar
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runAstar(startRiver, goalRiver):
   return 


######################################
## Input: string filename, list river
## Output: bool Success
######################################

def createOutputFile(fileName, river):
    fileExists = os.path.isfile(fileName)
    if fileExists:
        check = input("Are you sure you want to overwrite %s? (y,n) "%(fileName))
    else:
        check = "y"

    if check == "y":
        with open(fileName, 'w') as f:
            for line in river:
                f.write("%s\n" % line)
        return True
    else:
        return False


######################################
## Input: string fileName
## Output: list riverBank
######################################

def createRiverList(fileName):
    riverBank = readInputFile(fileName)
    if riverBank == False:
        print("Could not read from %s. Good bye"%(fileName))
    else:
        return riverBank


######################################
## Input: string fileName
## Returns: list riverLayout
######################################

def readInputFile(fileName):
    fileExists = os.path.isfile(fileName)
    if fileExists:
        with open(fileName) as f:
            lines = f.read().splitlines()
        return lines
    else:
        return False

######################################
## Input: None
## Output: None
######################################
def start():
    if (len(sys.argv) != 5):
        print("You entered %i"%(len(sys.argv)) + " argument(s)")
        print("Invalid number of arguments. Please enter in the following format:\n< initial state file > < goal state file > < mode > < output file >")
        exit()
    startRiver = createRiverList(str(sys.argv[1]))
    goalRiver = createRiverList(str(sys.argv[2]))
    mode = str(sys.argv[3])

    if mode == "bfs":
        runBfs(startRiver, goalRiver)
    elif mode == "dfs":
        print("nice")

    elif mode == "iddfs":
        print("nice")

    elif mode == "astar":
        print("nice")

    else:
        print("Uncompatable mode. Good bye.")
        exit()

    success = createOutputFile(str(sys.argv[4]), goalRiver)
    if success:
        print("%s successfully created. Good bye."%(str(sys.argv[4])))
    else:
        print("%s failed to be created. Good bye."%(str(sys.argv[4])))
        exit()



if __name__ == "__main__":
    start()
