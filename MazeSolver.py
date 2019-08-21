#################################################################
#                                                               #
#                   Author: Bilal Ahmed                         #
#                   Date: August 21, 2019                       #
#################################################################
from Map import Map

class Heap:
    def __init__(self):
        self.heap = [None] # Needs to be offset by 1 to resolve errors
        self.size = 0

    def insert(self, node, mp, speed, nodesSeen):
        self.size += 1  # Increment size
        self.heap.append(node)  # Add the node to the list
        self.bubble_up(mp, speed, nodesSeen)   # By property of heaps, we need to bubble_up the node at the end
    
    def extract_min(self, mp, speed, nodesSeen):
        result = self.heap[1]   # Extract min node
        self.heap[1] = self.heap[self.size] # Move node at end to the top
        self.size -= 1  # Decrement size of the heap
        self.heap.pop()
        self.bubble_down(1, mp, speed, nodesSeen) # Bubble-down the node at the very top

        return result
    
    def bubble_up(self, mp, speed, nodesSeen):
        index = self.size

        while(index > 1):
            
            if(nodesSeen[self.heap[index]] < nodesSeen[self.heap[index//2]]):
                self.swap_nodes(index, index//2)
            
            index = index//2
    
    def bubble_down(self, nodeIndex, mp, speed, nodesSeen):
        # While we still have children in the heap
        while(self.size >= (nodeIndex * 2)):
            leftChild = nodeIndex * 2
            rightChild = (nodeIndex * 2 + 1) if (nodeIndex*2 + 1 <= self.size - 1) else nodeIndex*2

            leftChildTime = nodesSeen[self.heap[leftChild]]
            rightChildTime = nodesSeen[self.heap[rightChild]]

            # If left child is less than right child, swap with left
            if(leftChildTime < rightChildTime):
                self.swap_nodes(leftChild, nodeIndex)
                nodeIndex = leftChild

            # else if right child is smaller or equal, swap with right
            elif (rightChildTime <= leftChildTime):
                self.swap_nodes(rightChild, nodeIndex)
                nodeIndex = rightChild

            # else, break because we can't percolate any lower
            else:
                break

    def swap_nodes(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]


def findPath(mp, speed):    

    result = dijkstra(mp, speed)

    timeToDest = result[0][(mp.sx-1, mp.sy-1)]  # Time to reach bottom-right from top-left
    pathToDest = result[1][(mp.sx-1, mp.sy-1)]  # The path taken to reach destination
    
    # Update path in mp
    mp.path = pathToDest

    return timeToDest


def dijkstra(mp, speed):
    
    # Create dictionary to store time from startPix
    nodesSeen = dict()
    pathsToNodes = dict()   # Store the a path for each pixel, which is the shortes possible path
    
    for i in range(mp.sx):
        for j in range(mp.sy):
            nodesSeen.update({(i,j) : float('inf')})
    
    # A heap to store the nodes that will be visited
    nodesToVisit = Heap()

    # Visit the first node and update time to visit for each
    nodesSeen.update({(0,0) : time(mp, speed, (0,0))})
    nodesSeen.update({(0,1) : time(mp, speed, (0,1)) + nodesSeen[(0,0)]})
    nodesSeen.update({(1,0) : time(mp, speed, (1,0)) + nodesSeen[(0,0)]})

    # Our best guesses to the two children of starting top-left node
    pathsToNodes.update({(0,1) : [(0,0)]})
    pathsToNodes.update({(1,0) : [(0,0)]})
    
    addNodeToHeap(nodesToVisit, (0,1), mp, speed, nodesSeen)
    addNodeToHeap(nodesToVisit, (1,0), mp, speed, nodesSeen)
    visited = set()
    count=0
    while(nodesToVisit.size > 0):

        # Pop the first element
        currNode =  nodesToVisit.extract_min(mp, speed, nodesSeen)
        if(currNode in visited):
            count+=1
        else:
            visited.add(currNode)
        topNeighbour = (currNode[0], currNode[1] - 1)
        rightNeighbour = (currNode[0] + 1, currNode[1])
        bottomNeighbour = (currNode[0], currNode[1] + 1)
        leftNeighbour = (currNode[0] - 1, currNode[1])

        # If we've reached the final node, break
        if (currNode == (mp.sx - 1, mp.sy - 1)):
            pathsToNodes.update({currNode : pathsToNodes[currNode] + [currNode]})   # Update location to destination pixel
            break

        '''***Update our best guess for time to neighbouring nodes, if required ***'''

        # Check if top neighbour exists, and update time
        if(currNode[1] - 1 >= 0):
            topNeighbourTime = time(mp, speed, topNeighbour)
            # If we have a faster way to get to this neighbour, update it and add them back to the Heap
            if(nodesSeen[currNode] + topNeighbourTime < nodesSeen[topNeighbour]):
                nodesSeen[topNeighbour] = nodesSeen[currNode] + topNeighbourTime
                pathsToNodes.update({topNeighbour : pathsToNodes[currNode] + [currNode]})
                addNodeToHeap(nodesToVisit, topNeighbour, mp, speed, nodesSeen)

        
        # Check if right neighbour exists, and update time
        if(currNode[0] + 1 <= mp.sx - 1):
            rightNeighbourTime = time(mp, speed, rightNeighbour)
            # If we have a faster way to get to this neighbour, update it and add them back to the Heap
            if(nodesSeen[currNode] + rightNeighbourTime < nodesSeen[rightNeighbour]):
                nodesSeen[rightNeighbour] = nodesSeen[currNode] + rightNeighbourTime
                pathsToNodes.update({rightNeighbour : pathsToNodes[currNode] + [currNode]})
                addNodeToHeap(nodesToVisit, rightNeighbour, mp, speed, nodesSeen)
        
        # Check if bottom neighbour exists, and update time
        if(currNode[1] + 1 <= mp.sy - 1):
            bottomNeighbourTime = time(mp, speed, bottomNeighbour)
            # If we have a faster way to get to this neighbour, update it and add them back to the Heap
            if(nodesSeen[currNode] + bottomNeighbourTime < nodesSeen[bottomNeighbour]):
                nodesSeen[bottomNeighbour] = nodesSeen[currNode] + bottomNeighbourTime
                pathsToNodes.update({bottomNeighbour : pathsToNodes[currNode] + [currNode]})
                addNodeToHeap(nodesToVisit, bottomNeighbour, mp, speed, nodesSeen)
        
        # Check if left neighbour exists, and update time
        if(currNode[0] - 1 >= 0):
            leftNeighbourTime = time(mp, speed, leftNeighbour)
            # If we have a faster way to get to this neighbour, update it and add them back to the Heap
            if(nodesSeen[currNode] + leftNeighbourTime < nodesSeen[leftNeighbour]):
                nodesSeen[leftNeighbour] = nodesSeen[currNode] + leftNeighbourTime
                pathsToNodes.update({leftNeighbour : pathsToNodes[currNode] + [currNode]})
                addNodeToHeap(nodesToVisit, leftNeighbour, mp, speed, nodesSeen)

    return [nodesSeen, pathsToNodes]


def addNodeToHeap(heap, nodeToAdd, mp, speed, nodesSeen):
    heap.insert(nodeToAdd, mp, speed, nodesSeen)    


def time(mp, speed, pix):
    return (1 / speed(mp, pix))


# Speed function(1)
# The speed at the pixel b is dependent on the amount of
# white it has.
def maze_speed(mp, p):
    pb = mp.pixels[p]
    dst = (pb[0])**2 + (pb[1])**2 + (pb[2])**2
    return ((dst/100.0) ** 0.5) + 0.01

if(__name__ == "__main__"):
    while True:

        # Promp for file path
        filePath = input("Enter path to PPM file (\'exit\' to exit): ")
        try:
            if(filePath == "exit"):
                break
            p = open(filePath)      # Check if file exists

        except:
            print("Error: Unable to open the file specified.")
            exit(1)
        
        # Run dijkstra implementation to find path to end
        try:
            inp = Map(filePath)
            path = findPath(inp, maze_speed)
            inp.outputPath()
            print("Finished! Check the \"output\" folder for results.")
        except:
            print("Error: Unable to find path.")
        
        del p   # Close file stream
        