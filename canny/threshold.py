#Remove this in the final version, not needed
from matplotlib import pyplot as plt
from skimage import exposure
import math
import numpy as np

class Queue():
    """Implementation of a queue (FIFO) data structure."""
    def __init__(self):
        #Initialise elements of queue
        self.elements=[]

    def __str__(self):
        #Initialise empty string
        string = ''

        #Convert each element into a co-ordinate representation
        for i in range(self.pointer,len(self.elements)+1):#test this
            element = elements[i]
            string += '('+str(element[0])+','+str(element[1])+'), '

        #Return the generated string
        return string

    def enqueue(self,val):
        #Add the new value to the queue
        self.elements.append(val)

    def dequeue(self):
        #Get the first element of the queue
        return self.elements.pop(0)

    def isEmpty(self):
        #If the length of the elements list is 0, it's empty
        if len(self.elements) == 0:
            return True
        else:
            return False

#Function to split a single dictionary into two, given a threshold
def splitDictionary(dictionary,threshold):
    #Initialise dictionaries
    low_dict = {}
    high_dict = {}

    #For all the key, value pairs in the input dictionary
    for key, value in dictionary.items():
        #If value is less than the split threshold, add it to low_dict
        if value < threshold:
            low_dict[key] = value
        #Otherwise, add it to high_dict
        else:
            high_dict[key] = value

    #Return the two new dictionaries
    return low_dict, high_dict

#Function to generate a histogram from a given image array
def generateHistogram(image):
    #Initialise dictionary
    hist={}

    #For all the pixels in the image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #Value is floor of pixel value
            val = math.floor(image[i][j])
            #If value not already in histogram, add it
            if val in hist:
                hist[val] += 1
            #Otherwise, increment it
            else:
                hist[val] = 1

    for i in range(min(list(hist.keys())), max(list(hist.keys()))):
        if i not in hist.keys():
            hist[i] = 0

    #Return generated histogram
    keys = list(hist.keys())
    values = list(hist.values())

    return keys, values

def cumulativeSum(array):
    weights = []
    for limit in range(len(array)):
        weight = 0
        if limit < len(array):
            for i in range(0, limit+1):
                weight += array[i]
        weights.append(weight)

    return weights

def otsuThreshold(image):
    pixVal, pixNo = generateHistogram(image)

    #Calculate cumulative sums for weight
    weight1 = cumulativeSum(pixNo)
    #Equivalent of weight2 = 1 - weight1
    weight2 = cumulativeSum(pixNo[::-1])[::-1]

    #Calculate pixNo * pixVal for all values in each
    pixNo_times_pixVal = [pixVal[i]*pixNo[i] for i in range(len(pixNo))]

    #Calculate means
    mean1 = [cumulativeSum(pixNo_times_pixVal)[i] / weight1[i] for i in range(len(weight1))]
    mean2 = [cumulativeSum(pixNo_times_pixVal[::-1])[i] / weight2[::-1][i] for i in range(len(weight2))][::-1]

    #Line up arrays
    weight1 = weight1[:-1]
    weight2 = weight2[1:]
    mean1 = mean1[:-1]
    mean2 = mean2[1:]

    #Calculate variances
    variances = []
    for i in range(len(weight1)):
        variances.append(weight1[i] * weight2[i] * (mean1[i] - mean2[i])**2)

    #Line up pixVal with variances list
    pixVal = pixVal[:-1]

    #Find optimal threshold
    optimalThreshold = pixVal[variances.index(max(variances))]

    return optimalThreshold

#Thresholding function
def threshold_image(image,low,high):
    #Initialise output array
    output = np.zeros(image.shape)

    #Initialise queue
    strongEdges = Queue()

    #For all pixels in the image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #If above the high threshold, the output pixel gets 255
            if image[i][j] >= high:
                output[i][j] = 255
                strongEdges.enqueue((i,j))
            #If below the low threshold, the output pixel gets 0
            elif image[i][j] < low:
                output[i][j] = 0
            #Otherwise, the output pixel gets 128
            else:
                output[i][j] = 128

    #Return thresholded image
    return output, strongEdges

def threshold(image, magnitude, suppressedImage, auto=True, lowThreshRatio=None,  highThreshRatio=None):
    if auto:
        #Calculate automatic threshold
        #Values are slightly manipulated since otsu generally over-estimates the threshold, these values give a better result
        highThresh = 0.8*otsuThreshold(image)
        lowThresh = 0.25*highThresh
    else:
        #NB highThreshRatio is a ratio OF max gradient magnitude
        #NB lowThreshRatio is a ratio OF highThreshRatio
        highThresh = highThreshRatio*np.max(magnitude)
        lowThresh = lowThreshRatio*highThresh

    #Threshold the image
    output, strongEdgesQueue = threshold_image(suppressedImage,lowThresh,highThresh)

    #Return thresholded image and queue of strong egdes
    return output, strongEdgesQueue
