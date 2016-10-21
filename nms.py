from __future__ import division
import math
import numpy as np

def checkExists(coordinates,shape):
    flag = 0
    for i in range(len(coordinates)):
            if coordinates[i] > shape[i]-1:
                flag = 1
    if flag == 1:
        return False
    else:
        return True

def non_maximum_suppression(magnitude,direction):
    #Create empty array of zeros to contain result
    output = np.zeros(magnitude.shape)

    #To shorten and neaten code;
    pi = math.pi

    #Iterate over image
    for y in range(magnitude.shape[0]):
        for x in range(magnitude.shape[1]):
            #To shorten and neaten code;
            theta = direction[y][x]
            shape = magnitude.shape

            if ((theta <= pi/4) and (theta > 0)) or (
                    (theta <= -3*pi/4) and (theta > -pi)):

                if checkExists((y-1,x+1),shape) and checkExists((y-1,x+1),shape):
                    #Calculate interpolated gradient /above/ the pixel
                    #Case: higher gradient > lower gradient
                    if magnitude[y-1][x+1] >= magnitude[y][x+1]:
                        upper_gradient = math.tan(theta)*(
                            magnitude[y-1][x+1] - magnitude[y][x+1]) + (
                                magnitude[y][x+1])

                    #Case: lower gradient > higher gradient
                    else:
                        upper_gradient = (1-math.tan(theta))*(
                            magnitude[y][x+1] - magnitude[y-1][x+1]) + (
                                magnitude[y-1][x+1])
                else:
                    upper_gradient = None

                if checkExists((y+1,x-1),shape) and checkExists((y,x-1),shape):
                    #Calculate inteporlated gradient /above/ the pixel
                    #Case: lower gradient > higher gradient
                    if magnitude[y+1][x-1] >= magnitude[y][x-1]:
                        lower_gradient = math.tan(theta)*(
                            magnitude[y+1][x-1] - magnitude[y][x-1]) + (
                                magnitude[y][x-1])

                    #Case: higher gradient > lower gradient
                    else:
                        lower_gradient = (1-math.tan(theta))*(
                            magnitude[y][x-1] - magnitude[y+1][x-1]) + (
                                magnitude[y+1][x-1])
                else:
                    lower_gradient = None


            elif ((theta <= pi/2) and (theta > pi/4)) or (
                    (theta <= -pi) and (theta > -3*pi/4)):

                if checkExists((y-1,x+1),shape) and checkExists((y-1,x),shape):
                    if magnitude[y-1][x+1] >= magnitude[y-1][x]:
                        upper_gradient = math.tan(pi/2-theta)*(
                            magnitude[y-1][x+1] - magnitude[y-1][x]) + (
                                magnitude[y-1][x])

                    else:
                        upper_gradient = (1-math.tan(pi/2-theta))*(
                            magnitude[y-1][x] - magnitude[y-1][x+1]) + (
                                magnitude[y-1][x+1])
                else:
                    upper_gradient = None

                if checkExists((y+1,x-1),shape) and checkExists((y+1,x),shape):
                    if magnitude[y+1][x-1] >= magnitude[y+1][x]:
                        lower_gradient = math.tan(pi/2-theta)*(
                            magnitude[y+1][x-1] - magnitude[y+1][x]) + (
                                magnitude[y+1][x])

                    else:
                        lower_gradient = (1-math.tan(pi/2-theta))*(
                            magnitude[y+1][x] - magnitude[y+1][x-1]) + (
                                magnitude[y+1][x-1])
                else:
                    lower_gradient = None

            elif ((theta <= 0) and (theta > -pi/4)) or (
                    (theta <= pi) and (theta > 3*pi/4)):

                if checkExists((y+1,x+1),shape) and checkExists((y,x+1),shape):
                    if magnitude[y+1][x+1] >= magnitude[y][x+1]:
                        lower_gradient = math.tan(-theta)*(
                            magnitude[y+1][x+1] - magnitude[y][x+1]) + (
                                magnitude[y][x+1])

                    else:
                        lower_gradient = (1-math.tan(-theta))*(
                            magnitude[y][x+1] - magnitude[y+1][x+1]) + (
                                magnitude[y+1][x+1])
                else:
                    lower_gradient = None

                if checkExists((y-1,x-1),shape) and checkExists((y,x-1),shape):
                    if magnitude[y-1][x-1] >= magnitude[y][x-1]:
                        upper_gradient = math.tan(-theta)*(
                            magnitude[y-1][x-1] - magnitude[y][x-1]) + (
                                magnitude[y][x-1])

                    else:
                        upper_gradient = (1-math.tan(-theta))*(
                            magnitude[y][x-1] - magnitude[y-1][x-1]) + (
                                magnitude[y-1][x-1])
                else:
                    upper_gradient = None

            elif ((theta <= -pi/4) and (theta > -pi/2)) or (
                    (theta <= 3*pi/4) and (theta > pi/2)):

                if checkExists((y+1,x+1),shape) and checkExists((y+1,x),shape):
                    if magnitude[y+1][x+1] >= magnitude[y+1][x]:
                        lower_gradient = math.tan(pi/2 + theta)*(
                           magnitude[y+1][x+1] - magnitude[y+1][x]) + (
                               magnitude[y+1][x])

                    else:
                        lower_gradient = (1-math.tan(pi/2+theta))*(
                            magnitude[y+1][x] - magnitude[y+1][x+1]) + (
                                magnitude[y+1][x+1])
                else:
                    lower_gradient = None

                if checkExists((y-1,x-1),shape) and checkExists((y-1,x),shape):
                    if magnitude[y-1][x-1] >= magnitude[y-1][x]:
                        upper_gradient = math.tan(pi/2+theta)*(
                            magnitude[y-1][x-1] - magnitude[y-1][x]) + (
                                magnitude[y-1][x])

                    else:
                        upper_gradient =  (1-math.tan(pi/2+theta))*(
                            magnitude[y-1][x] - magnitude[y-1][x-1]) + (
                                magnitude[y-1][x-1])
                else:
                    upper_gradient = None

            #Need to deal with upper_gradient or lower_gradient being None
            if (upper_gradient == None) and (lower_gradient != None):
                if magnitude[y][x] >= lower_gradient:
                    output[y][x] = 255
                else:
                    output[y][x] = 0
            elif (upper_gradient != None) and (lower_gradient == None):
                if magnitude[y][x] >= upper_gradient:
                    output[y][x] = 255
                else:
                    output[y][x] = 0
            elif (upper_gradient == None) and (lower_gradient == None):
                print('fuck')
                output[y][x] = 255
            elif (magnitude[y][x] >= upper_gradient) and (
                magnitude[y][x] >= lower_gradient):
                output[y][x] = 255
            else:
                output[y][x] = 0
    return output
