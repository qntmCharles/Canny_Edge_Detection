"""
Created on Sun Jul 31 12:57:42 2016

@author: qntmCharles
"""
from __future__ import division
from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

from convolution import convolution
from gaussian import G,gaussiankernel
from sobel import sobel
from plot import plot
from nms import non_maximum_suppresion

def main():
    I = np.asarray(Image.open('test.png').convert('L'),dtype=np.float32)
    #np.savetxt('image.txt',np.around(I,3),fmt='%.2f',delimiter='|')
    g = gaussiankernel(0.5,5)
    gaussian_result = convolution(I,g,'extend')
    #Image.fromarray(gaussian_result.astype(np.uint8)).show()
    #np.savetxt('gaussian.txt',np.around(a,3),fmt='%.2f',delimiter='|',newline='EOL')
    #np.savetxt('sobel.txt',np.around(b,3),delimiter='|')
    sobel_result_gradient,sobel_result_direction,sobel_result_direction2 = sobel(gaussian_result)
    #plt.imshow(sobel_result_gradient,cmap='gist_rainbow',interpolation='nearest')
    #plt.show()
    plot(sobel_result_direction2)
    #Image.fromarray(sobel_result_gradient.astype(np.uint8)).show()
    suppressed_image = non_maximum_suppresion(sobel_result_gradient,sobel_result_direction)
    #Image.fromarray(suppressed_image).show()

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
