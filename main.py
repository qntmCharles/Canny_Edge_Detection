"""
Created on Sun Jul 31 12:57:42 2016

@author: CharlesP
"""
from __future__ import division
from PIL import Image
import numpy as np
import math

from convolution import convolution
from gaussian import G,gaussiankernel

def sobel(image):
    h = np.array([[ 1, 2, 1],
                  [ 0, 0, 0],
                  [-1,-2,-1]])

    v = np.array([[ 1, 0,-1],
                  [ 2, 0,-2],
                  [ 1, 0,-1]])

    rh = convolution(image, v, 'extend')
    rv = convolution(image, h, 'extend')
    # Debug: save horizontal and vertical sobel convolutions
    #np.savetxt('rh.txt',rh)
    #np.savetxt('rv.txt',rv)

    edge_gradient = np.zeros(image.shape)
    gradient_direction = np.zeros(image.shape)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            edge_gradient[y][x] = math.sqrt(rh[y][x]**2 + rv[y][x]**2)
            gradient_direction[y][x] = math.atan2(rv[y][x],rh[y][x])
    return 255.*np.absolute(edge_gradient)/np.max(edge_gradient), gradient_direction

def main():
    I = np.asarray(Image.open('test.png').convert('L'),dtype=np.float32)
    np.savetxt('image.txt',np.around(I,3),fmt='%.2f',delimiter='|')
    g = gaussiankernel(2,5)
    gaussian_result = convolution(I,g,'extend')
    Image.fromarray(gaussian_result.astype(np.uint8)).show()
    #np.savetxt('gaussian.txt',np.around(a,3),fmt='%.2f',delimiter='|',newline='EOL')   
    #np.savetxt('sobel.txt',np.around(b,3),delimiter='|')    
    sobel_result_gradient,sobel_result_direction = sobel(gaussian_result)
    #Perhaps plot gradient direction?
    Image.fromarray(sobel_result_gradient.astype(np.uint8)).show()
    

if __name__ == '__main__':
    main()


#########
"""sobel (works - just doesn't look as it will at the end)
I = np.asarray(Image.open('test.png').convert('L'),dtype=np.float32)
print(I.shape)
g = np.array(gaussiankernel(3,5))
a = convolution(I,g,'extend')
g = np.array([[1,0,-1],
          [2,0,-2],
          [1,0,-1]])
r = convolution(a,g,'extend')
r = 255.0*np.absolute(r)/np.max(r)
final = Image.fromarray(r.round().astype(np.uint8))
final.show()"""


############
"""gaussian (definitely works)
I = np.asarray(Image.open('pigeon.jpg'),dtype=np.float32)

Image.fromarray(r.round().astype(np.uint8)).show()"""
