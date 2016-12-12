from __future__ import division
import math
from decimal import *
import numpy as np
getcontext().prec=15

def checkExists(coordinates,shape):
    for i in range(len(coordinates)):
        if (coordinates[i] > shape[i%2] - 1) or (coordinates[i] < 0):
            return False
    return True

def interpolate(hVector,vVector,x1,x2):
    #x1 is bottom
    difference = (vVector/hVector)*abs(x2-x1)
    if x2 > x1:
        result = x1+difference
    else:
        result = x1-difference

    if (result > max(x1,x2)) and not (math.isclose(max(x1,x2),result)):
        print('Error')
        print(result)
    elif (result < min(x1,x2)) and not (math.isclose(min(x1,x2),result)):
        print('Error')
        print(result)
    else:
        return result

def displayRegion(y,x,mag,shape):
    a=[[],[],[]]
    for i in range(-1,2):
        for j in range(-1,2):
            if checkExists((y+i,x+j),shape):
                a[i+1].append(mag[y+i][x+j])
            else:
                a[i+1].append('-')
    for row in a:
        print(row)

def nonMaximumSuppression(mag,magH,magV,direction):
    output = np.zeros(direction.shape)

    pi = math.pi

    for y in range(direction.shape[0]):
        for x in range(direction.shape[1]):
            angle = direction[y][x]
            h = magH[y][x]
            v = magV[y][x]
            shape = mag.shape
            #displayRegion(y,x,mag,shape)

            if angle == pi:
                index = 7
            else:
                index=math.floor((angle+pi)/(2*pi)*8)

            #\   |   /
            # \ 6|5 /
            #7 \ | / 4
            #_________
            #
            #0 / | \ 3
            # / 1|2 \
            #/   |   \


            if index == 0:
                if checkExists((y,x-1,y+1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-h,-v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x+1,y-1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-h,-v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 1:
                if checkExists((y+1,x,y+1,x-1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-v,-h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y-1,x,y-1,x+1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-v,-h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 2:
                if checkExists((y+1,x,y+1,x+1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-v,h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y-1,x,y-1,x-1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-v,h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 3:
                if checkExists((y,x+1,y+1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(h,-v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x-1,y-1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(h,-v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 4:
                if checkExists((y,x+1,y-1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(h,v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x-1,y+1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(h,v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 5:
                if checkExists((y-1,x,y-1,x+1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(v,h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y+1,x,y+1,x-1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(v,h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 6:
                if checkExists((y-1,x,y-1,x-1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(v,-h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y+1,x,y+1,x+1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(v,-h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 7:
                if checkExists((y,x-1,y-1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-h,v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x+1,y+1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-h,v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            else:
                print('Error: unclassified angle (',angle,')')
            #print('Angle: ',angle*180/pi, 'Index: ',index)
            #print('Sobel (h,v): ', h, v)
            #print(gradient1, gradient2)
            if (gradient1 != None) and (gradient2 != None):
                if (mag[y][x] > gradient1) and (mag[y][x] > gradient2):
                   output[y][x] = mag[y][x]
                   #print('Maximum')
                else:
                    output[y][x] = 0
                    #print('Not maximum')
            elif gradient1 != None:
                if mag[y][x] > gradient1:
                    output[y][x] = mag[y][x]
                    #print('Maximum')
                else:
                    output[y][x] = 0
                    #print('Not maximum')
            elif gradient2 != None:
                if mag[y][x] > gradient2:
                    output[y][x] = mag[y][x]
                    #print('Maximum')
                else:
                    output[y][x] = 0
                    #print('Not maximum')
            else:
                output[y][x] = mag[y][x]
                #print('Maximum')

            #if y > 60:
                #input()

    return output
