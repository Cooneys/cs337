import sys
import os


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
    river = [[0,0,0]]
    if (len(sys.argv) != 5):
        print("You entered %i"%(len(sys.argv)) + " argument(s)")
        print("Invalid number of arguments. Please enter in the following format:\n< initial state file > < goal state file > < mode > < output file >")
        exit()
    startRiver = createRiverList(str(sys.argv[1]))
    goalRiver = createRiverList(str(sys.argv[2]))

    success = createOutputFile(str(sys.argv[4]), goalRiver)
    if success:
        print("%s successfully created. Good bye."%(str(sys.argv[4])))
    else:
        print("%s failed to be created. Good bye."%(str(sys.argv[4])))



if __name__ == "__main__":
    start()
