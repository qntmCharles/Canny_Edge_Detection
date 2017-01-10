import math
import numpy as np
from .queueClass import Queue

#Function to split a single dictionary into two, given a threshold
def splitDictionary(dictionary,threshold):
    """
        Function to split a single dictionary 'dictionary' into two given
        a threshold

        NB: this function assumes that the input dictionary's keys are all
        integers: this is checked in the assert statement
    """

    # Check that the keys are all integers
    for key in dictionary.keys():
        assert isinstance(key,int) or isinstance(key,str), \
                'Dictionary keys contain non-integer'

    # Initialise dictionaries
    lowDict = {}
    highDict = {}

    # For all the key, value pairs in the input dictionary
    for key, value in dictionary.items():
        # If value is less than the split threshold, add it to lowDict
        if value < threshold:
            lowDict[key] = value

        # Otherwise, add it to highDict
        else:
            highDict[key] = value

    return lowDict, highDict

#Function to generate a histogram from a given image array
def generateHistogram(image):
    """
        Function to generate a histogram from a given array 'image'

        NB: keys are the items that have been identified in the image,
        values are the counts for each item

        NB: function converts all numbers in the array to the largest
        integer less than or equal
    """
    # Initialise empty dictionary
    hist={}

    # For all the pixels in the image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Value is floor of pixel value
            val = math.floor(image[i][j])

            # Check value is now an integer
            assert isinstance(val, int), 'Non-integer key'

            # If value not already in histogram, add it
            if val in hist:
                hist[val] += 1

            # Otherwise, increment the count for this key
            else:
                hist[val] = 1


    # This checks that the keys of the histogram form a full interval,
    # i.e. any missing values between the min and max key values are entered
    # with counts of 0
    for i in range(min(list(hist.keys())), max(list(hist.keys()))):
        if i not in hist.keys():
            hist[i] = 0

    # Return histograms as seperate key and value lists
    keys = list(hist.keys())
    values = list(hist.values())

    return keys, values

def cumulativeSum(array):
    """
        Function to calculate the cumulative sum through an array
    """
    # Initialise empty list
    sums = []

    #For each 'stopping point' (limit) up to the end of the array
    for limit in range(len(array)):
        # Initialise sum for this limit as 0
        currentSum = 0

        # Iterate through the items up to and including the limit and sum
        for i in range(0, limit+1):
            currentSum += array[i]

        #Add sum to list
        sums.append(currentSum)

    return sums

def otsuThreshold(image):
    """
        Function to perform otsu thresholding on a given array 'image'
    """
    # Get the pixel values and counts for local variable image
    pixVal, pixNo = generateHistogram(image)

    # Calculate cumulative sums for weight
    weight1 = cumulativeSum(pixNo)

    # weight2 = 1 - weight1
    weight2 = cumulativeSum(pixNo[::-1])[::-1]

    # Calculate pixNo * pixVal for all values in each
    pixNoTimesPixVal = [pixVal[i]*pixNo[i] for i in range(len(pixNo))]

    #Calculate means
    mean1 = [cumulativeSum(pixNoTimesPixVal)[i] / weight1[i] for i in \
            range(len(weight1))]
    mean2 = [cumulativeSum(pixNoTimesPixVal[::-1])[i] / weight2[::-1][i] \
            for i in range(len(weight2))][::-1]

    # Line up arrays (the last value of weight1 & mean1 is not needed, thus
    # the first in weight2 & mean2)
    weight1 = weight1[:-1]
    weight2 = weight2[1:]
    mean1 = mean1[:-1]
    mean2 = mean2[1:]

    #Calculate variances
    variances = []
    for i in range(len(weight1)):
        variances.append(weight1[i] * weight2[i] * (mean1[i] - mean2[i])**2)

    # Line up pixVal with variances list
    pixVal = pixVal[:-1]

    # Find optimal threshold
    optimalThreshold = pixVal[variances.index(max(variances))]

    return optimalThreshold

def thresholdImage(image,low,high):
    """
        Function to threshold an array given a low and high threshold,
        returning the thresholded image as an array

        NB: the choice of 255 for a strong edge, 128 for a candidate and 0 for
        no edge is arbitrary. It is simply for easy testing, since 255 and 128
        are noticeably different and 0 is simply black (it should also be
        noted, however, that in the final image a strong edge *should* be 255)
    """
    # Initialise output array
    output = np.zeros(image.shape)

    # Initialise queue
    strongEdges = Queue()

    # Iterate over image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # If above the high threshold, the output pixel gets 255
            if image[i][j] >= high:
                output[i][j] = 255
                #Add pixel coordinates to queue
                strongEdges.enqueue((i,j))

            # If below the low threshold, the output pixel gets 0
            elif image[i][j] < low:
                output[i][j] = 0
            # Otherwise, the output pixel gets 128
            else:
                output[i][j] = 128

    return output, strongEdges

def thresholdInterface(image, magnitude, suppressedImage, auto, \
        lowThreshRatio=None, highThreshRatio=None):
    """
        Function that acts as an interface between the thresholding algorithm
        and the rest of the program, takes image, gradient magnitude and
        suppressed image array, as well as a boolean to indicate whether otsu
        thresholding will be used. If necessary, also takes a low and high
        threshold ratio

        Returns the thresholded image as an array

        NB highThreshRatio is a ratio OF max gradient magnitude

        NB lowThreshRatio is a ratio OF highThreshRatio
    """
    #Check low and high threshold ratios are floats between 0 and 1
    if lowThreshRatio != None:
        assert isinstance(lowThreshRatio, float), 'threshold ratio must \
                be a float'

        assert (lowThreshRatio >= 0) and (lowThreshRatio <= 1), 'threshold \
                must be between 0 and 1 inclusive'

    if highThreshRatio != None:
        assert isinstance(highThreshRatio, float), 'threshold ratio \
                must be a float'

        assert (highThreshRatio >= 0) and (highThreshRatio <= 1), 'threshold \
                must be between 0 and 1 inclusive'

    #If automatic thresholding
    if auto:
        highThresh = 0.8*otsuThreshold(image)
        lowThresh = 0.25*highThresh

    #Otherwise, convert low and high threshold ratios to actual thresholds
    else:
        highThresh = highThreshRatio*np.max(magnitude)
        lowThresh = lowThreshRatio*highThresh

    # Threshold the image
    output, strongEdgesQueue = thresholdImage(suppressedImage,lowThresh,highThresh)

    return output, strongEdgesQueue
