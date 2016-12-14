import math
import numpy as np
from .convolution import convolution

def calculateValue(x,y,sigma):
    #Return value from gaussian distribution formula for x,y
    return (1/(2*math.pi*(sigma**2)))*(math.e**(-(x**2 + y**2)/(2*sigma**2)))

def generateKernel(sigma,width):
    #Calculate radius of kernel
    radius = int((width-1)/2)

    #Create empty array of required size
    kernel = np.zeros((width,width))

    #Iterate through arrays
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            #Approximate value from gaussian distribution
            kernel[y+radius][x+radius] = calculateValue(x,y,sigma)

    #Normalize kernel
    kernel = kernel/np.sum(kernel)

    return kernel

def gaussian(sigma,width,image):
    kernel = generateKernel(sigma,width)
    output = convolution(image,kernel)
    return output
