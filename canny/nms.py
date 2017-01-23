from __future__ import division
import math
import numpy as np

def checkExists(coordinates,shape):
    """
        Function that check if a list of co-ordinate tuples (local variable
        coordinates) is within the dimensions of local variable shape

        NB: local variable shape is a tuple of image dimensions
    """
    # For each item in the list of coordinates
    for i in range(len(coordinates)):
        # If coordinate is larger than it's corresponding image dimension
        # or less than 0
        if (coordinates[i] > shape[i%2] - 1) or (coordinates[i] < 0):
            return False

    # If False is not yet returned, return True
    return True

def interpolate(hVector,vVector,x1,x2):
    """
        Function that performs linear interpolation using local variables
        hVector and vVector, between local variables x1 and x2

        NB: interpolation is performed assuming hVector and vVector are
        positive, that is, the interpolation is in the first quadrant, with
        x1 and x2 forming the side of a triangle parallel to the y-axis,
        with the angle at the origin being equal to arctanvVector/hVector)
        NB: x1 is assumed to be geometrically 'lower' than x2, i.e. on the
        x-axis
    """
    # Calculate the interpolated difference, i.e. how much the interpolateed
    # value should be different from x2 or x1
    difference = (vVector/hVector)*abs(x2-x1)

    # If x2 is larger than x1, difference is above x1
    if x2 > x1:
        result = x1+difference
    # Otherwise below x1
    else:
        result = x1-difference

    # If the resulting point is larger than the largest of x1 and x2, or
    # smaller than the smallest, then there has been an error
    # math.isclose determines if they're close, i.e. the result is only just
    # outside of the range (x1,x2) - this can occur due to floating point
    # errors
    if (result > max(x1,x2)) and not (math.isclose(max(x1,x2),result,\
            abs_tol=1e-09)):
        print(x1, x2, result)
        print('Error: interpolated point greater than original points.')

    elif (result < min(x1,x2)) and not (math.isclose(min(x1,x2),result,\
            abs_tol=1e-09)):
        print(difference)
        print(x1, x2, result)
        print('Error: interpolated point less than original points.')

    # If it is not one of the above cases, the resulting point is okay and the
    # result may be returned
    else:
        return result

def displayRegion(y,x,mag):
    """
        Function for displaying the region around a point in the array (x,y)
        for testing purposes

        Takes the point x, y, and the array 'mag' containing the gradient
        magnitude array

        Returns nothing, only prints the region
    """
    # Initialise a list with 3 nested lists to contain the region
    region = [[],[],[]]

    # Get dimensions of magnitude array
    shape = mag.shape()

    # Iterate over the region
    for i in range(-1,2):
        for j in range(-1,2):
            # If the current place in the region is in the image, add it's
            # value to the region array
            if checkExists((y+i,x+j),shape):
                region[i+1].append(mag[y+i][x+j])

            #Otherwise add '-' to signify an absent value
            else:
                region[i+1].append('-')

    #Print the array row by row
    for row in region:
        print(row)

def nonMaximumSuppression(mag,magH,magV,direction):
    """
        Function that performs non-maximum suppression on the local variable
        mag containing the gradient magnitude array, as well as magH,
        containing the horizontal gradient components, magV, containing the
        vertical components, and direction, containing the gradient directions

        Returns array of 0s (suppressed) and the original magnitude otherwise
    """
    # Initialise array of zeros for output
    output = np.zeros(direction.shape)

    # To neaten and shorten code (without obfuscation!)
    pi = math.pi
    shape = mag.shape

    # Iterate over the image
    for y in range(direction.shape[0]):
        for x in range(direction.shape[1]):
            #Get the angle, horizontal and vertical components of the gradient
            angle = direction[y][x]
            h = magH[y][x]
            v = magV[y][x]
            #displayRegion(y,x,mag)

            # Map the angle from continuous -pi < angle <= pi to discrete
            # 0 <= index <= 7
            # Angle = pi is a special case to avoid dividing by zero (index
            # could be 0 or 7, 7 was chosen so that
            # lowerBound < angle <= upperBound is satisfied
            if angle == pi:
                index = 7
            else:
                index=math.floor((angle+pi)/(2*pi)*8)

            #\   |   /
            # \ 6|5 /
            #7 \ | / 4
            #_________
            #
            #0 / | \ 3
            # / 1|2 \
            #/   |   \

            # For each index, the horizontal and vertical gradient components,
            # as well as the pixels, are mapped as if they have index 4, since
            # the linear interpolation function works as if this is where
            # the interpolation is taking place

            if index == 0:
                # Check if the points required are within the image
                if checkExists((y,x-1,y+1,x-1),shape):
                    # Get values of pixels being used for interpolation
                    pixels=(mag[y][x-1],mag[y+1][x-1])

                    # If the above pixel values are the same, then any
                    # interpolated point will also be the same
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]

                    #Otherwise, interpolate to find the gradient magnitude
                    else:
                        gradient1 = interpolate(-h,-v,pixels[0],pixels[1])

                # If the points are not both present, set gradient to 0, in
                # the interest of finding all edges
                else:
                    gradient1 = 0

                #Check if the points required are within the image
                if checkExists((y,x+1,y-1,x+1),shape):
                    # Get vcalues of pixels being used for interpolation
                    pixels=(mag[y][x+1],mag[y-1][x+1])

                    # If the above pixel values are the same, then any
                    # interpolated point will also be the same
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]

                    #Otherwise, interpolate to the find the gradient magnitude
                    else:
                        gradient2 = interpolate(-h,-v,pixels[0],pixels[1])

                # If the points are not both present, set gradient to 0, in
                # the interest of finding all edges
                else:
                    gradient2 = 0

            elif index == 1:
                if checkExists((y+1,x,y+1,x-1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-v,-h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y-1,x,y-1,x+1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-v,-h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 2:
                if checkExists((y+1,x,y+1,x+1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-v,h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y-1,x,y-1,x-1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-v,h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 3:
                if checkExists((y,x+1,y+1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(h,-v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x-1,y-1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(h,-v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 4:
                if checkExists((y,x+1,y-1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(h,v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x-1,y+1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(h,v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 5:
                if checkExists((y-1,x,y-1,x+1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(v,h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y+1,x,y+1,x-1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(v,h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 6:
                if checkExists((y-1,x,y-1,x-1),shape):
                    pixels=(mag[y-1][x],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(v,-h,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y+1,x,y+1,x+1),shape):
                    pixels=(mag[y+1][x],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(v,-h,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            elif index == 7:
                if checkExists((y,x-1,y-1,x-1),shape):
                    pixels=(mag[y][x-1],mag[y-1][x-1])
                    if pixels[0] == pixels[1]:
                        gradient1 = pixels[0]
                    else:
                        gradient1 = interpolate(-h,v,pixels[0],pixels[1])
                else:
                    gradient1 = 0

                if checkExists((y,x+1,y+1,x+1),shape):
                    pixels=(mag[y][x+1],mag[y+1][x+1])
                    if pixels[0] == pixels[1]:
                        gradient2 = pixels[0]
                    else:
                        gradient2 = interpolate(-h,v,pixels[0],pixels[1])
                else:
                    gradient2 = 0

            # If the index is not any of the above, then it is unclassified
            else:
                print('Error: unclassified angle ('+str(angle)+')')

            # If either of the gradient magnitudes is None (i.e has had an
            # error) then give benefit of the doubt and set as candidate
            if (gradient1 is None) or (gradient2 is None):
                output[y][x] = mag[y][x]

            # If the gradient magnitude of the current pixel is larger than
            # both interpolated gradient magnitudes, it is a maximum, and
            # thus it's pixel value is kept
            elif (mag[y][x] > gradient1) and (mag[y][x] > gradient2):
               output[y][x] = mag[y][x]

            #Otherwise, the output for this pixel is 0
            else:
                output[y][x] = 0

    return output
