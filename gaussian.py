from __future__ import division
import math 
import numpy as np

def G(x,y,sigma):
    return (1/(2*math.pi*(sigma**2)))*(math.e**(-(x**2 + y**2)/(2*sigma**2)))
    
def gaussiankernel(sigma,width):
    radius = int((width-1)/2)
    kernel = np.zeros((width,width))
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            kernel[y+radius][x+radius] = G(x,y,sigma)
    kernel = kernel/np.sum(kernel)
    return kernel