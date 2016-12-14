from .nms import checkExists
import numpy as np
import math

class Queue():
    """Implementation of a queue (FIFO) data structure."""
    def __init__(self):
        #Initialise elements of queue
        self.elements=[]

    def __str__(self):
        #Initialise empty string
        string = ''

        #Convert each element into a co-ordinate representation
        for i in range(self.pointer,len(self.elements)+1):#test this
            element = elements[i]
            string += '('+str(element[0])+','+str(element[1])+'), '

        #Return the generated string
        return string

    def enqueue(self,val):
        #Add the new value to the queue
        self.elements.append(val)

    def dequeue(self):
        #Get the first element of the queue
        return self.elements.pop(0)

    def isEmpty(self):
        #If the length of the elements list is 0, it's empty
        if len(self.elements) == 0:
            return True
        else:
            return False

def findConnectedEdges(mag, y, x):
    for i in range(-2,3):
        for j in range(-2,3):
            if checkExists((y+i, x+j),mag.shape):
                #This can be combined into one if
                if mag[y+i][x+j] == 128:
                    mag[y+i][x+j] = 255
                    mag = findConnectedEdges(mag, y+i, x+j)
    return mag

def hysteresis(image, strongEdges):
    while not strongEdges.isEmpty():
        coords = strongEdges.dequeue()
        output = findConnectedEdges(image, coords[0], coords[1])
    """#Initialise queue and list of stsrong edges
    toVisit = Queue()
    edges = []

    #For all pixels in the image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #If the pixel has a value of 255 and isn't already an edge
            if (image[i][j] == 255) and ((i,j) not in edges):
                #Add to queue and list of edges
                edges.append((i,j))
                toVisit.enqueue((i,j))
                #Go through queue until empty
                while not toVisit.isEmpty():
                    #Dequeue first element
                    coord = toVisit.dequeue()
                    #Check in a 3*3 area around the pixel for connectivity
                    for y in range(-1,2):
                        for x in range(-1,2):
                            #To neaten code;
                            current = (coord[0]+y,coord[1]+x)

                            #If the pixel exists
                            if checkExists(current,image.shape):
                                val = image[coord[0]+y][coord[1]+x]
                                #If the pixel is a strong/potential edge
                                if (val == 255) or (val == 128):
                                    if current not in edges:
                                        #Add to queue and list of edges
                                        toVisit.enqueue(current)
                                        edges.append(current)

    #Initialise final output array
    output = np.zeros(image.shape)"""

    #For all pixels in the image, if it's an edge, assign 255
    #Any pixel that isn't an edge remains 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if output[i][j] != 255:
                output[i][j] = 0


    #Return final output array
    return output



