import sys
import os
import queue
import heapq

nodeCount = 0
depthLimit = 0
mode = ''
possibleSuccessors = [[1,0],[2,0],[0,1],[1,1],[0,2]]


######################################
## input: tuple result
## output: list path
######################################

def pathToGoal(result):
    node = result[0]
    path = []
    count = 0
    while True:
        try:
            if node.parent == None:
                break
            path.append(node.action)
            count += 1
        except:
            break
        node = node.parent
    return count, path[::-1]

######################################
## input: tuple action, Node node
## output: Successor
######################################

def executeAction(action, node):
    if node.state.leftBank[2] == 1:
        return Successor(list(node.state.leftBank), list(node.state.rightBank), action, 1)
    else:
        return Successor(list(node.state.rightBank), list(node.state.leftBank), action, 0)
    

######################################
## input: tuple action, Node node
## output: bool state.legal()
######################################

def checkAction(action, node):
    if node.state.leftBank[2] == 1:
        startBank = list(node.state.leftBank)
        endBank = list(node.state.rightBank)
    else:
        endBank = list(node.state.leftBank)
        startBank = list(node.state.rightBank)
        

    startBank[0] -= action[0]
    startBank[1] -= action[1]
    endBank[0] += action[0]
    endBank[1] += action[1]

    if startBank[0] >= 0 and startBank[1] >= 0 and endBank[0] >= 0 and endBank[1] >= 0 \
        and ((startBank[0] == 0) or (startBank[0] >= startBank[1])) \
        and ((endBank[0] == 0) or (endBank[0] >= endBank[1])):
        return True
    else:
        return False


######################################
## input: Node node
## output: list successors
######################################

def listSuccessors(node):
    successors = [] 
    if ((mode == 'iddfs') and (node.depth == depthLimit)):
        successors = [] 
    else:
        legalActions = list(filter(lambda i: checkAction(i, node), possibleSuccessors))
        validSuccessors = map(lambda j: executeAction(j, node), legalActions)
    for each in validSuccessors:
        temp = Node(each.state, node, node.depth+1, each.action, node.depth+1)
        successors.append(temp)
    return successors

######################################
## Class: Node
## input: State state, Node parent, tuple action, int pathCost
######################################

class Successor():
    def __init__(self, startBank, endBank, action, boatSide):
        startBank[0] -= action[0]
        startBank[1] -= action[1]
        endBank[0] += action[0]
        endBank[1] += action[1]
        self.action = action
        
        if boatSide == 1:
            self.rightBank = endBank
            self.leftBank = startBank
            self.rightBank[2] = 1
            self.leftBank[2] = 0
        elif boatSide == 0:
            self.rightBank = startBank
            self.leftBank = endBank
            self.rightBank[2] = 0
            self.leftBank[2] = 1

        self.state = State(self.leftBank, self.rightBank)

######################################
## Class: Node
## input: State state, Node parent, tuple action, int pathCost
######################################

class Node():
    def __init__(self, state, parent=None, depth=0, action=None, pathCost=0):
        global nodeCount
        self.state = state
        self.parent = parent
        self.depth = depth
        self.action = action
        self.pathCost = pathCost
        self.check = tuple(self.state.leftBank + self.state.rightBank)
        nodeCount += 1


######################################
## Class: State
## input: list river
######################################

class State():
    def __init__(self, river, extra=0):
        if (extra == 0):
            self.leftBank = river[0].split(",")
            self.rightBank = river[1].split(",")
            for each in range(len(self.leftBank)):
                self.leftBank[each] = int(self.leftBank[each])
            for each in range(len(self.rightBank)):
                self.rightBank[each] = int(self.rightBank[each])
        else:
            self.leftBank = river
            self.rightBank = extra

    def printState(self):
        print("Left Bank: %s chickens, %s wolves, %s boat"%(self.leftBank[0], self.leftBank[1], self.leftBank[2]), end=" - ")
        print("Right Bank: %s chickens, %s wolves, %s boat"%(self.rightBank[0], self.rightBank[1], self.rightBank[2]))

    def legal(self):
        if self.leftBank[0] <= 0:
            return False 
        if self.leftBank[1] <= 0:
            return False 

        for each in [self.rightBank[0], self.rightBank[1]]:
            if each <= 0:
                return False 
                
        if self.leftBank[0] <= self.leftBank[1]:
            return False 
        if self.rightBank[0] <= self.rightBank[1]:
            return False 
        if self.leftBank[2] + self.rightBank[2] != 1:
            return False 

        return True



######################################
## Mode: bfs
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runBfs(startRiver, goalRiver):
    if goalRiver.leftBank == startRiver.leftBank and goalRiver.rightBank == startRiver.rightBank:
        return startRiver, 0
    nodeCounter = 0
    frontier = queue.Queue()
    explored = set()
    frontier.put(Node(startRiver))

    i = 0
    while frontier.qsize() > 0:
        i += 1
        currentRiver = frontier.get()
        explored.add(currentRiver.check)
        children = listSuccessors(currentRiver)
        for each in children:
            nodeCounter += 1
            if each.check not in explored:
                if (goalRiver.leftBank == each.state.leftBank) and (goalRiver.rightBank == each.state.rightBank):
                    return each, nodeCounter
                frontier.put(each)
        

######################################
## Mode: dfs
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runDfs(startRiver, goalRiver):
    if goalRiver.leftBank == startRiver.leftBank and goalRiver.rightBank == startRiver.rightBank:
        return startRiver, 0
    nodeCounter = 0
    frontier = queue.LifoQueue()
    explored = set()
    frontier.put(Node(startRiver))

    i = 0
    while frontier.qsize() > 0:
        i += 1
        currentRiver = frontier.get()
        explored.add(currentRiver.check)
        children = listSuccessors(currentRiver)
        for each in children:
            nodeCounter += 1
            if each.check not in explored:
                if (goalRiver.leftBank == each.state.leftBank) and (goalRiver.rightBank == each.state.rightBank):
                    return each, nodeCounter
                frontier.put(each)


######################################
## Mode: iddfs
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runIddfs(startRiver, goalRiver):
    nodeCounter = 0
    for depthLimit in range(500):
        result = dls(startRiver, goalRiver, nodeCounter, depthLimit)
        if result != "cutoff": 
            return result
    print("Solution not found!")
    exit()


def dls(startRiver, goalRiver, nodeCounter, depthLimit):
    return rDls(Node(startRiver), goalRiver, nodeCounter, depthLimit)

def rDls(node, goalRiver, nodeCounter, depthLimit):
    if goalRiver.leftBank == node.state.leftBank and goalRiver.rightBank == node.state.rightBank:
        return node, nodeCounter
    elif depthLimit == 0:
        return "cutoff"
    cutoff = False
    for each in listSuccessors(node):
        nodeCounter += 1
        result = rDls(each, goalRiver, nodeCounter, depthLimit-1)
        if result == "cutoff":
            cutoff = True
        elif result:
            return result
    if cutoff == True:
        return "cutoff"
    else:
        return False


######################################
## Mode: astar
## Input: string startRiver, string goalRiver
## Output: list outputRiver
######################################

def runAstar(startRiver, goalRiver):
    if goalRiver.leftBank == startRiver.leftBank and goalRiver.rightBank == startRiver.rightBank:
        return startRiver, 0
    nodeCounter = 0
    frontier = PriorityQueue()
    explored = set()
    frontier.put(cost(startRiver, goalRiver), Node(startRiver))
    
    while True:
        if frontier.lengt() == 0:
            print("Solution not found!")
            exit()
        currentRiver = frontier.get()
        explored.add(currentRiver.check)
        for each in listSuccessors(currentRiver):
            nodeCounter += 1
            if each.check not in explored:
                if goalRiver.leftBank == currentRiver.state.leftBank and goalRiver.rightBank == currentRiver.state.rightBank:
                    return currentRiver, nodeCounter
                frontier.put(cost(each.state, goalRiver), each)

def cost(riverBank, goalRiver):
    if goalRiver.rightBank == 1:
        #divide by two for amount of boat riders in one trip
        cost = (riverBank.leftBank[0] + riverBank.leftBank[1]) / 2 
    else:
        cost = (riverBank.rightBank[0] + riverBank.rightBank[1]) / 2
    return cost


class PriorityQueue:
    def __init__(self):
        self.pqueue = []
        self.index = 0

    def lengt(self):
        return len(self.pqueue)

    def put(self, priority, node):
        heapq.heappush(self.pqueue, (priority, self.index, node))
        self.index += 1

    def get(self):
        return heapq.heappop(self.pqueue)[-1]

######################################
## Input: string filename, list river
## Output: bool Success
######################################

def createOutputFile(fileName, path, nodeCount):
    fileExists = os.path.isfile(fileName)
    if fileExists:
        check = input("Are you sure you want to overwrite %s? (y,n) "%(fileName))
    else:
        check = "y"

    if check == "y":
        with open(fileName, 'w') as f:
            f.write("The amount of crossings in the path: %i\n"%(path[0]))
            f.write("The total number of expanded nodes is: %s\n"%(nodeCount))
            f.write("And the path is:\n")
            for each in path[1]:
                f.write("%s\n"% each)
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
        exit()
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
    startRiver = State(createRiverList(str(sys.argv[1])))
    goalRiver = State(createRiverList(str(sys.argv[2])))
    mode = str(sys.argv[3])

    if mode == "bfs":
        result = runBfs(startRiver, goalRiver)
    elif mode == "dfs":
        result = runDfs(startRiver, goalRiver)

    elif mode == "iddfs":
        result = runIddfs(startRiver, goalRiver)

    elif mode == "astar":
        result = runAstar(startRiver, goalRiver)

    else:
        print("Uncompatable mode. Good bye.")
        exit()

    path = pathToGoal(result)
    print("The amount of crossings needed: %i\nThe path is: \n %s \n And the total number of expanded nodes is: %s"%(path[0], path[1], result[1]))

    success = createOutputFile(str(sys.argv[4]), path, result[1])
    if success:
        print("%s successfully created. Good bye."%(str(sys.argv[4])))
    else:
        print("%s failed to be created. Good bye."%(str(sys.argv[4])))
        exit()



if __name__ == "__main__":
    start()
