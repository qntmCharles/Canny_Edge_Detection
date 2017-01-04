from .nms import checkExists
from .queueClass import Queue
import numpy as np
import math, sys

def findConnectedEdges(mag, y, x):
    """

    for i in range(-2,3):
        for j in range(-2,3):
            if checkExists((y+i, x+j),mag.shape):
                #This can be combined into one if
                if mag[y+i][x+j] == 128:
                    mag[y+i][x+j] = 255
                    mag = findConnectedEdges(mag, y+i, x+j)
    return mag

def hysteresis(image, strongEdges):
    sys.setrecursionlimit(image.shape[0]*image.shape[1])
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



