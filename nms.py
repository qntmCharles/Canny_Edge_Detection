import math
import numpy as np

def non_maximum_suppresion(magnitude, direction):
    output = np.zeros(magnitude.shape)
    for y in range(magnitude.shape[0]):
        for x in range(magnitude.shape[1]):
            if direction[y][x] == '0':
                if y <= 0:
                    pass #Edge case
                elif y >= magnitude.shape[0] - 1:
                    pass #Edge case
                else:
                    if (magnitude[y][x] > magnitude[y+1][x]) and (
                            magnitude[y][x] > magnitude[y-1][x]):
                        output[y][x] = 255
                    else:
                        output[y][x] = 0
            elif direction[y][x] == '45':
                if (x <= 0) and (y <= 0):
                    pass #Edge case
                elif (x >= magnitude.shape[1] - 1) and (
                        y >= magnitude.shape[0] - 1):
                    pass #Edge case
                elif x <= 0:
                    pass #Edge case
                elif y>= magnitude.shape[0] - 1:
                    pass #Edge case
                elif x >= magnitude.shape[1] - 1:
                    pass #Edge case
                elif y <= 0:
                    pass #Edge case
                else:
                    if (magnitude[y][x] > magnitude[y+1][x-1]) and (
                            magnitude[y][x] > magnitude[y-1][x+1]):
                        output[y][x] = 255
                    else:
                        output[y][x] = 0
            elif direction[y][x] == '90':
                if x <= 0:
                    pass #Edge case
                elif x >= magnitude.shape[1] - 1:
                    pass #Edge case
                else:
                    if (magnitude[y][x] > magnitude[y][x+1]) and (
                            magnitude[y][x] > magnitude[y][x-1]):
                        output[y][x] = 255
                    else:
                        output[y][x] = 0
            elif direction[y][x] == '135':
                if (x <= 0) and (y>=magnitude.shape[0]):
                    pass #Edge case
                elif (x >= magnitude.shape[1] - 1) and (y <= 0):
                    pass #Edge case
                elif x <= 0:
                    pass #Edge case
                elif y>= magnitude.shape[0] - 1:
                    pass #Edge case
                elif x >= magnitude.shape[1] - 1:
                    pass #Edge case
                elif y <= 0:
                    pass #Edge case
                else:
                    if (magnitude[y][x] > magnitude[y+1][x+1]) and (
                            magnitude[y][x] > magnitude[y-1][x-1]):
                        output[y][x] = 255
                    else:
                        output[y][x] = 0
            else:
                print("Uncategorised direction: ",y,x, direction[y][x])

    return output
