from __future__ import division
import math
import numpy as np
channels=1
def convolution(I,g,mode):
    if g.shape[0] != g.shape[1]:
        print('Kernel must be symmetric.')
    if mode == 'extend':
        r = np.zeros(I.shape)
        pad = int(math.floor(g.shape[0]/2))
        for y in range(I.shape[0]):
            for x in range(I.shape[1]):
                if (y-pad<0 and x-pad<0): #Top left corner              
                    p=0                    
                    bufx = pad-x
                    bufy = pad-y
                    a=np.zeros(g.shape)
                    for i in range(-pad+bufy,pad+1): #Fill array
                        for j in range(-pad+bufx,pad+1):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    for i in range(0,bufy): #Replace pixels beyond edge
                        for j in range(0,bufx):
                            a[i][j] = a[bufy][bufx]
                    for i in range(bufy,g.shape[0]):
                        for j in range(0,bufx):
                            a[i][j] = a[i][bufx]
                    for i in range(0,bufy):
                        for j in range(bufx,g.shape[0]):
                            a[i][j] = a[bufy][j]
                    for i in range(0,g.shape[0]): #Convolute
                        for j in range(0,g.shape[0]):
                            p+=a[i][j] * g[i][j]
                    r[y][x]=p
                elif (y-pad<0 and x+pad>=I.shape[1]): #Top right corner
                    p=0
                    bufx = pad-(I.shape[1]-1-x) 
                    bufy = pad-y
                    a=np.zeros(g.shape)
                    for i in range(-pad+bufy,pad+1):
                        for j in range(-pad,pad+1-bufx):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    for i in range(0,bufy): #Replace pixels beyond edge
                        for j in range(0,bufx):
                            a[i][j] = a[bufy][j]
                    for i in range(0,bufy):
                        for j in range(bufx,g.shape[0]):
                            a[i][j] = a[bufy][bufx]
                    for i in range(bufy,g.shape[0]):
                        for j in range(bufx,g.shape[0]):
                            a[i][j] = a[i][bufx]
                    for i in range(0,g.shape[0]): #Convolute
                        for j in range(0,g.shape[0]):
                            p+=a[i][j] * g[i][j]
                    r[y][x]=p 
                elif (y+pad>=I.shape[0] and x+pad>=I.shape[1]): #Bottom right corner
                    p=0
                    bufx=pad-(I.shape[1]-1-x)
                    bufy=pad-(I.shape[0]-1-y)
                    a=np.zeros(g.shape)
                    for i in range(-pad,pad+1-bufy): #Fill array
                        for j in range(-pad,pad+1-bufx):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    #Replace pixels beyond edge
                    for i in range(0,g.shape[0]-bufy): 
                        for j in range(g.shape[1]-bufx,g.shape[1]):          
                            a[i][j] = a[i][g.shape[1]-bufx-1]
                    for i in range(g.shape[0]-bufy,g.shape[0]):
                        for j in range(g.shape[1]-bufx,g.shape[1]):
                            a[i][j] = a[g.shape[0]-bufy-1][g.shape[1]-bufx-1]
                    for i in range(g.shape[0]-bufy,g.shape[0]):
                        for j in range(0,g.shape[1]-bufx):
                            a[i][j] = a[g.shape[0]-bufy-1][j]
                    for i in range(0,g.shape[0]): #Convolute
                        for j in range(0,g.shape[0]):
                            p+=a[i][j] * g[i][j]
                    r[y][x]=p
                elif (y+pad>=I.shape[0] and x-pad<0): #Bottom left corner
                    p=0
                    bufx=pad-x
                    bufy=pad-(I.shape[0]-1-y)
                    a=np.zeros(g.shape)
                    for i in range(-pad,pad+1-bufy): #Fill array
                        for j in range(-pad+bufx,pad+1):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    for i in range(0,g.shape[0]-bufy): #Replace pixels beyond edge
                        for j in range(0,bufx):
                            a[i][j] = a[i][bufx]
                    for i in range(g.shape[0]-bufy,g.shape[0]):
                        for j in range(0,bufx):
                            a[i][j] = a[g.shape[0]-bufy-1][bufx]
                    for i in range(g.shape[0]-bufy,g.shape[0]):
                        for j in range(bufx,g.shape[0]):
                            a[i][j] = a[g.shape[0]-bufy-1][j]
                    for i in range(0,g.shape[0]): #Convolute
                        for j in range(0,g.shape[0]):
                            p+=a[i][j] * g[i][j]
                    r[y][x]=p 
                elif y-pad<0 or y+pad>I.shape[0]-1: #Horizontal
                    p=0                    
                    if y-pad<0: #Top horizontal
                        bufy = pad-y
                        a=np.zeros(g.shape) #3 for RGB channels
                        for i in range(-pad+bufy,pad+1): #Fill array
                            for j in range(-pad,pad+1):
                                a[i+pad][j+pad] = I[y+i][x+j]
                        for i in range(0,bufy): #Replace pixels beyond edge
                            for j in range(0,g.shape[0]):
                                a[i][j] = a[bufy][j]
                    if y+pad>=I.shape[0]: #Bottom horizontal
                        bufy = pad-(I.shape[0]-1-y)
                        a=np.zeros(g.shape) #3 for RGB channels
                        for i in range(-pad, pad+1-bufy): #Fill array
                            for j in range(-pad, pad+1):
                                a[i+pad][j+pad] = I[y+i][x+j]
                        for i in range(g.shape[0]-bufy,g.shape[0]): #Replace pixels beyond edge
                            for j in range(0, g.shape[0]):
                                a[i][j] = a[g.shape[0]-1-bufy][j]
                    for i in range(0,g.shape[0]): #Convolute
                        for j in range(0,g.shape[0]):
                            p+=a[i][j] * g[i][j]
                    r[y][x]=p
                elif x-pad<0 or x+pad>I.shape[1]-1: #Vertical
                    p=0                    
                    if x-pad<0: #Left vertical
                        bufx = pad-x
                        a=np.zeros(g.shape) #3 for RGB channels
                        for i in range(-pad,pad+1): #Fill array
                            for j in range(-pad+bufx,pad+1):
                                a[i+pad][j+pad] = I[y+i][x+j]
                        for i in range(0,g.shape[0]): #Replace pixels beyond edge
                            for j in range(0,bufx):
                                a[i][j] = a[i][bufx]
                    if x+pad>I.shape[1]-1: #Right vertical
                        bufx = pad-(I.shape[1]-1-x)
                        a=np.zeros(g.shape)
                        for i in range(-pad,pad+1): #Fill array
                            for j in range(-pad,pad+1-bufx):
                                a[i+pad][j+pad] = I[y+i][x+j]
                        for i in range(0,g.shape[0]): #Replace pixels beyond edge
                            for j in range(g.shape[0]-bufx,g.shape[0]):
                                a[i][j] = a[i][g.shape[0]-bufx-1]                                
                    for i in range(0,g.shape[0]): #Convolute
                        for j in range(0,g.shape[0]):
                            p+=a[i][j] * g[i][j]
                    r[y][x]=p
                else:
                    p = 0
                    for i in range(-pad,pad+1):
                        for j in range(-pad,pad+1):
                            p+=I[y+i][x+j] * g[i+pad][j+pad]
                    r[y][x] = p
    if mode == 'wrap':
        pass
    if mode == 'zero':
        pass
    if mode == 'crop':
        pass
    return r