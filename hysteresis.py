from __future__ import division
from nms import checkExists
import numpy as np
import math

class Queue():
    def __init__(self):
        self.frames=[]

    def __str__(self):
        string = ''
        for frame in self.frames:
            string += '('+str(frame[0])+','+str(frame[1])+'), '
        return string


    def enqueue(self,val):
        self.frames.append(val)

    def dequeue(self):
        val = self.frames[0]
        self.frames = self.frames[1:]
        return val

    def empty(self):
        if len(self.frames) == 0:
            return True
        else:
            return False

def hysteresis(image):
    toVisit = Queue()
    edges = []

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == 255) and ((i,j) not in edges):
                edges.append((i,j))
                toVisit.enqueue((i,j))
                while not toVisit.empty():
                    coord = toVisit.dequeue()
                    for y in range(-1,2):
                        for x in range(-1,2):
                            current = (coord[0]+y,coord[1]+x)
                            if checkExists(current,image.shape):
                                val = image[coord[0]+y][coord[1]+x]
                                if (val == 255) or (val == 128):
                                    if current not in edges:
                                       toVisit.enqueue(current)
                                       edges.append(current)
    output = np.zeros(image.shape)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i,j) in edges:
                output[i][j] = 255

    return output



