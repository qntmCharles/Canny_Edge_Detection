from .nms import checkExists
from .queueClass import Queue
import numpy as np
import math, sys

def findConnectedEdges(mag, y, x):
    """
        Function that searches a 5x5 area focused on a single point in the
        image before recursively calling the function for other points that
        contain an edge, taking the gradient magnitude array and the point
        coordinates

        Returns the updated gradient magnitude array

        NB: this is depth-first connectivity searching (is that the fancy name?

        NB: uses 8-connectivity: an edge can be connected from either side

        NB: allowing a 5x5 area rather than the typical 3x3 provides better
        results - a gap of a single pixel is hardly noticeable
    """
    # Iterate over 5x5 area around point (x,y)
    for i in range(-2,3):
        for j in range(-2,3):

            # If the current point exists and is an edge candidate
            if checkExists((y+i, x+j),mag.shape) and (mag[y+i][x+j] == 128):

                # Update the point to a strong edge
                mag[y+i][x+j] = 255

                # Recursively call the function for this point
                mag = findConnectedEdges(mag, y+i, x+j)

    return mag

def hysteresis(image, strongEdges):
    """
        Function that performs threshold hysteresis on the input array 'image'
        using the queue of known strong edges 'strongEdges'

        Returns the array with hysteresis complete: this is the final image

        NB: In the mostextreme case, every pixel in the image may be
        considered an edge, thus recursion could happen as far as all pixels,
        thus a new recursion limit must be set
    """
    # Set recursion limit
    sys.setrecursionlimit(image.shape[0]*image.shape[1])

    # While there are still strong edges to check
    while not strongEdges.isEmpty():
        # Get coordinates as a tuple from the queue
        coords = strongEdges.dequeue()

        # Find any connected edges around the strong edge
        output = findConnectedEdges(image, coords[0], coords[1])

    # Remove unconnected edge candidates
    # Iterate over the image
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            # If pixel is an edge candidate (which by this point must be
            # unconnected), set to 0
            if output[i][j] == 128:
                output[i][j] = 0

    return output

def oldHysteresis(image, strongEdges):
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
    output = np.zeros(image.shape)

    #For all pixels in the image, if it's an edge, assign 255
    #Any pixel that isn't an edge remains 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if output[i][j] != 255:
                output[i][j] = 0


    #Return final output array
    return output



