import math
import numpy as np
from .convolution import convolution

def calculateValue(x, y, sigma):
    """
        Function that returns the value from the discrete gaussian
        distribution formula for point (x,y)
    """
    # Check that x and y are integers
    assert type(x) is int, 'x must be an integer'
    assert type(y) is int, 'y must be an integer'

    return (1/(2*math.pi*(sigma**2)))*(math.e**(-(x**2 + y**2)/(2*sigma**2)))

def generateKernel(sigma, width):
    """
        Function that generate a kernel for gaussian blur, takes a standard
        deviation and kernel width

        Returns a gaussian blur kernel of the specified width as an array
    """
    # Check that kernel width is odd
    assert width % 2 == 1, 'kernel width must be an odd integer'

    # Calculate radius of kernel
    radius = int((width-1)/2)

    # Create empty array of required size
    kernel = np.zeros((width,width))

    # Iterate through arrays
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            # Approximate value from gaussian distribution
            kernel[y+radius][x+radius] = calculateValue(x,y,sigma)

    # Normalise kernel
    kernel = kernel/np.sum(kernel)

    return kernel

def gaussianInterface(sigma,width,image):
    """
        Function that acts as an interface between the gaussian blur algorithm
        and the rest of the program, takes standard deviation and kernel width
        to be passed to generateKernel, and an image to pass to convolution

        Returns image with gaussian blur applied as an array
    """
    # Generate kernel for blur
    kernel = generateKernel(sigma,width)

    # Convolve kernel and image
    output = convolution(image,kernel)

    return output
