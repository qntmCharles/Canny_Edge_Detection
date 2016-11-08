from __future__ import division
from nms import checkExists
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
        for element in self.elements:
            string += '('+str(element[0])+','+str(element[1])+'), '

        #Return the generated string
        return string

    def enqueue(self,val):
        #Add the new value to the queue
        self.elements.append(val)

    def dequeue(self):
        #Get the first element of the queue
        val = self.elements[0]
        #Remove the first element
        self.elements = self.elements[1:]
        return val

    def empty(self):
        #If the length of the elements list is 0, it's empty
        if len(self.elements) == 0:
            return True
        else:
            return False

def hysteresis(image):
    #Initialise queue and list of stsrong edges
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
                while not toVisit.empty():
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
    output = np.zeros(image.shape)

    #For all pixels in the image, if it's an edge, assign 255
    #Any pixel that isn't an edge remains 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i,j) in edges:
                output[i][j] = 255

    #Return final output array
    return output



