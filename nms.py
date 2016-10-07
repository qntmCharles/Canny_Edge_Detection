import math
import numpy as np

def non_maximum_suppresion(gradient_magnitude, gradient_direction):
    output = np.zeros(gradient_magnitude.shape)
    for y in range(gradient_magnitude.shape[0]):
        for x in range(gradient_magnitude.shape[1]):
            if gradient_direction[y][x] == 0:
                if x <= 0:
                    pass #Edge case
                elif x >= gradient_magnitude.shape[1] - 1:
                    pass #Edge case
                else:
                    pass
            if gradient_direction[y][x] == 45:
                pass
            if gradient_direction[y][x] == 90:
                if y <= 0:
                    pass #Edge case
                elif y >= gradient_magnitude.shape[0] - 1:
                    pass #Edge case
                else:
                    pass
            if gradient_direction[y][x] == 135:
                pass
            else:
                print("Uncategorised direction: ",y,x)

                """
                if gradient_direction[y][x] == 90:
                    if (gradient_magnitude[y][x] > gradient_magnitude[y][x-1]) and (gradient_magnitude[y][x] > gradient_magnitude[y][x+1]):
                        output[y][x] = 255
                    else:
                        output[y][x] = 0
                if gradient_direction[y][x] == 0:
                    if (gradient_magnitude[y][x] > gradient_magnitude[y-1][x]) and (gradient_magnitude[y][x] > gradient_magnitude[y+1][x]):
                        output[y][x] = 255
                    else:
                        output[y][x] = 0
"""
    #Need some kind of edge handling. What should happen when the
    #check goes over the edge? Simply ignore the other side?
    return output


