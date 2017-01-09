import math
import numpy as np

def convolution(I,k):
    """
        Function for 2-D convolution of two arrays

        NB: local variable I is the image being convolved

        NB: local variable k is the kernel

        NB: 'edge', here, refers to the edge of the image, not the edges
            being detected

        NB: uses 'extend' method for edge handling: extend image values beyond
            edge

        NB: python does not have arrays, only lists of lists. Where I refer to
        an array, I am referring to a numpy array
    """

    #Check if kernel is symmetrical
    if k.shape[0] != k.shape[1]:
        print('Kernel must be symmetric.')

    #Create array of zeros with the same size as image
    r = np.zeros(I.shape)

    #Calculate no. pixels to not need edge handling (kernel radius)
    pad = int(math.floor(k.shape[0]/2))

    #Iterate over image
    for y in range(I.shape[0]):
        for x in range(I.shape[1]):

            #Edge handling for top left corner
            if (y-pad<0 and x-pad<0):
                #Set pixel total to 0
                p=0
                #Calculate no. pixels over edge in x and y
                bufx = pad-x
                bufy = pad-y
                #Create array of zeros to fill for convolution
                a=np.zeros(k.shape)
                #For the pixels that aren't over the edge, fill the array
                for i in range(-pad+bufy,pad+1):
                    for j in range(-pad+bufx,pad+1):
                        a[i+pad][j+pad] = I[y+i][x+j]
                #Fill array by extending top left corner
                for i in range(0,bufy):
                    for j in range(0,bufx):
                        a[i][j] = a[bufy][bufx]
                #Fill array by extending left side
                for i in range(bufy,k.shape[0]):
                    for j in range(0,bufx):
                        a[i][j] = a[i][bufx]
                #Fill array by extending top side
                for i in range(0,bufy):
                    for j in range(bufx,k.shape[1]):
                        a[i][j] = a[bufy][j]
                #Convolve as normal
                for i in range(0,k.shape[0]): #Convolute
                    for j in range(0,k.shape[0]):
                        p+=a[i][j] * k[i][j]
                #Place calculated value in result array
                r[y][x]=p

            #Edge handling for top right corner
            elif (y-pad<0 and x+pad>=I.shape[1]):
                #Set pixel total to 0
                p=0
                #Calculate no. pixels over edge in x and y
                bufx = pad-(I.shape[1]-1-x)
                bufy = pad-y
                #Create array of zeros to fill for convolution
                a=np.zeros(k.shape)
                #For the pixels that aren't over the edge, fill the array
                for i in range(-pad+bufy,pad+1):
                    for j in range(-pad,pad+1-bufx):
                        a[i+pad][j+pad] = I[y+i][x+j]
                #Fill array by extending top side
                for i in range(0,bufy):
                    for j in range(0,k.shape[1]+1-bufx):
                        a[i][j] = a[bufy][j]
                #Fill array by extending top right corner
                for i in range(0,bufy):
                    for j in range(k.shape[1]-bufx,k.shape[1]):
                        a[i][j] = a[bufy][bufx]
                #Fill array by extending right side
                for i in range(bufy,k.shape[0]):
                    for j in range(k.shape[1]-bufx, k.shape[1]):
                        a[i][j] = a[i][k.shape[1]-1-bufx]
                #Convolve as normal
                for i in range(0,k.shape[0]): #Convolute
                    for j in range(0,k.shape[0]):
                        p+=a[i][j] * k[i][j]
                #Place calculated value in result array
                r[y][x]=p

            #Edge handling for bottom right corner
            elif (y+pad>=I.shape[0] and x+pad>=I.shape[1]):
                #Set pixel total to 0
                p=0
                #Calculate no. pixels over edge in x and y
                bufx=pad-(I.shape[1]-1-x)
                bufy=pad-(I.shape[0]-1-y)
                #Create array of zeros to fill for convolution
                a=np.zeros(k.shape)
                #For pixels that aren't over the edge, fill the array
                for i in range(-pad,pad+1-bufy):
                    for j in range(-pad,pad+1-bufx):
                        a[i+pad][j+pad] = I[y+i][x+j]
                #Fill array by extending right side
                for i in range(0,k.shape[0]-bufy):
                    for j in range(k.shape[1]-bufx,k.shape[1]):
                        a[i][j] = a[i][k.shape[1]-bufx-1]
                #Fill array by extending bottom right corner
                for i in range(k.shape[0]-bufy,k.shape[0]):
                    for j in range(k.shape[1]-bufx,k.shape[1]):
                        a[i][j] = a[k.shape[0]-bufy-1][k.shape[1]-bufx-1]
                #Fill array by extending bottom side
                for i in range(k.shape[0]-bufy,k.shape[0]):
                    for j in range(0,k.shape[1]-bufx):
                        a[i][j] = a[k.shape[0]-bufy-1][j]
                #Convolve as normal
                for i in range(0,k.shape[0]):
                    for j in range(0,k.shape[0]):
                        p+=a[i][j] * k[i][j]
                #Place calculated value in result array
                r[y][x]=p

            #Edge handling for bottom left corner
            elif (y+pad>=I.shape[0] and x-pad<0):
                #Set pixel total to 0
                p=0
                #Calculate no. pixels over edge in x and y
                bufx=pad-x
                bufy=pad-(I.shape[0]-1-y)
                #Create array of zeros to fill for convolution
                a=np.zeros(k.shape)
                #For pixels that aren't over the edge, fill the array
                for i in range(-pad,pad+1-bufy):
                    for j in range(-pad+bufx,pad+1):
                        a[i+pad][j+pad] = I[y+i][x+j]
                #Fill array by extending left side
                for i in range(0,k.shape[0]-bufy):
                    for j in range(0,bufx):
                        a[i][j] = a[i][bufx]
                #Fill array by extending bottom left corner
                for i in range(k.shape[0]-bufy,k.shape[0]):
                    for j in range(0,bufx):
                        a[i][j] = a[k.shape[0]-bufy-1][bufx]
                #Fill array by extending bottom side
                for i in range(k.shape[0]-bufy,k.shape[0]):
                    for j in range(bufx,k.shape[0]):
                        a[i][j] = a[k.shape[0]-bufy-1][j]
                #Convolve as normal
                for i in range(0,k.shape[0]):
                    for j in range(0,k.shape[0]):
                        p+=a[i][j] * k[i][j]
                #Place calculated value in result array
                r[y][x]=p

            #Edge handling for top and bottom sides
            elif y-pad<0 or y+pad>I.shape[0]-1:
                #Set pixel total to 0
                p=0
                #Edge handling for top side
                if y-pad<0:
                    #Calculate no. pixels over edge in y
                    bufy = pad-y
                    #Create array of zeros to fill for convolution
                    a=np.zeros(k.shape)
                    #For pixels that aren't over the edge, fill array
                    for i in range(-pad+bufy,pad+1):
                        for j in range(-pad,pad+1):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    #Fill array by extending top side
                    for i in range(0,bufy):
                        for j in range(0,k.shape[0]):
                            a[i][j] = a[bufy][j]

                #Edge handling for bottom side
                if y+pad>=I.shape[0]:
                    #Calculate no. pixels over edge in y
                    bufy = pad-(I.shape[0]-1-y)
                    #Create array of zeros to fill for convolution
                    a=np.zeros(k.shape)
                    #For pixels that aren't over the edge, fill array
                    for i in range(-pad, pad+1-bufy):
                        for j in range(-pad, pad+1):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    #Fill array by extending bottom side
                    for i in range(k.shape[0]-bufy,k.shape[0]):
                        for j in range(0, k.shape[0]):
                            a[i][j] = a[k.shape[0]-1-bufy][j]

                #Convolve as normal
                for i in range(0,k.shape[0]):
                    for j in range(0,k.shape[0]):
                        p+=a[i][j] * k[i][j]
                #Place calculated value in result array
                r[y][x]=p

            #Edge handling for left and right sides
            elif x-pad<0 or x+pad>I.shape[1]-1:
                #Set pixel total to 0
                p=0
                #Edge handling for left side
                if x-pad<0:
                    #Calculate no. pixels over edge in x
                    bufx = pad-x
                    #Create array of zeros to fill for convolution
                    a=np.zeros(k.shape)
                    #For pixels that aren't over the edge, fill array
                    for i in range(-pad,pad+1):
                        for j in range(-pad+bufx,pad+1):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    #Fill array by extending left side
                    for i in range(0,k.shape[0]):
                        for j in range(0,bufx):
                            a[i][j] = a[i][bufx]

                #Edge handling for right side
                if x+pad>I.shape[1]-1:
                    #Calculate no. pixels over edge in x
                    bufx = pad-(I.shape[1]-1-x)
                    #Create array of zeros to fill for convolution
                    a=np.zeros(k.shape)
                    #For pixels that aren't over the edge, fill array
                    for i in range(-pad,pad+1):
                        for j in range(-pad,pad+1-bufx):
                            a[i+pad][j+pad] = I[y+i][x+j]
                    #Fill array by extending right side
                    for i in range(0,k.shape[0]):
                        for j in range(k.shape[0]-bufx,k.shape[0]):
                            a[i][j] = a[i][k.shape[0]-bufx-1]

                #Convolve as normal
                for i in range(0,k.shape[0]):
                    for j in range(0,k.shape[0]):
                        p+=a[i][j] * k[i][j]

                #Place calculated value in result array
                r[y][x]=p

            #For all other pixels, convolve as normal
            else:
                #Set pixel total, p, to 0
                p = 0
                #Iterate over kernel
                for i in range(-pad,pad+1):
                    for j in range(-pad,pad+1):
                        #Multiple kernel with pixel, then add to total
                        p+=I[y+i][x+j] * k[i+pad][j+pad]
                #Place calculated value in result array
                r[y][x] = p

    return r
