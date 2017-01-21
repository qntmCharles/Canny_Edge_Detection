from .nms import checkExists
from .queueClass import Queue
import numpy as np
import math, sys, time

def findConnectedEdges(array, y, x):
    """
        Function that searches a 5x5 area focused on a single point in the
        iarraye before recursively calling the function for other points that
        contain an edge, taking the gradient magnitude array and the point
        coordinates

        Returns the updated array

        NB: this is depth-first connectivity searching (is that the fancy name?

        NB: uses 8-connectivity: an edge can be connected from either side

        NB: allowing a 5x5 area rather than the typical 3x3 provides better
        results - a gap of a single pixel is hardly noticeable
    """
    # Iterate over 5x5 area around point (x,y)
    for i in range(-2,3):
        for j in range(-2,3):

            # If the current point exists and is an edge candidate
            if checkExists((y+i, x+j),array.shape) and (array[y+i][x+j] == 128):

                # Update the point to a strong edge
                array[y+i][x+j] = 255

                # Recursively call the function for this point
                array = findConnectedEdges(array, y+i, x+j)

    return array

def hysteresis(image, strongEdges):
    """
        Function that performs threshold hysteresis on the input array 'image'
        using the queue of known strong edges 'strongEdges'

        Returns the array with hysteresis complete: this is the final image

        NB: In the most extreme case, every pixel in the image may be
        considered an edge, thus recursion could happen as far as all pixels,
        thus a new recursion limit must be set
    """

    # Prevent original image from being edited
    image = np.copy(image)

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
