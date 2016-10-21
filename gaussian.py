from __future__ import division
import math
import numpy as np

def G(x,y,sigma):
    #Return value from gaussian distribution formula for x,y
    return (1/(2*math.pi*(sigma**2)))*(math.e**(-(x**2 + y**2)/(2*sigma**2)))

def gaussiankernel(sigma,width):
    #Calculate radius of kernel
    radius = int((width-1)/2)

    #Create empty array of required size
    kernel = np.zeros((width,width))

    #Iterate through arrays
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            #Approximate value from gaussian distribution
            kernel[y+radius][x+radius] = G(x,y,sigma)

    #Normalize kernel
    kernel = kernel/np.sum(kernel)

    return kernel
