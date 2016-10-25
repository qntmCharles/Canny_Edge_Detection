from __future__ import division
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
    labels = []
    toVisit = Queue()
    edges = []

    #Initialise coordinates
    i=0
    j=0

    while i < image.shape[0]:
        while j < image.shape[1]:
            #print('Now on pixel: ',i,j)
            if (image[i][j] == 255) and ((i,j) not in edges):
                #print('Now working on: ',i,j)
                edges.append((i,j))
                toVisit.enqueue((i,j))
                while not toVisit.empty():
                    current = toVisit.dequeue()
                    #print('Current focus: ',current)
                    for y in range(-1,2):
                        for x in range(-1,2):
                            #print(current[0]+y,current[1]+x)
                            try:
                                if (image[current[0]+y][current[1]+x] == 255) or (
                                       image[current[0]+y][current[1]+x] == 128):
                                    if (current[0]+y,current[1]+x) not in edges:
                                       toVisit.enqueue((current[0]+y,current[1]+x))
                                       #print('Enqueued')
                                       edges.append((current[0]+y,current[1]+x))
                                       #print('Edge list: ',edges)
                                       #print('Queue: ',toVisit)
                                       #input()
                            except:
                                print(current[0]+y,current[1]+x)
                j+=1
            else:
                j+=1
        i+=1
        j=0

    output = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i,j) in edges:
                output[i][j] = 255
    #print(edges)
    return output



