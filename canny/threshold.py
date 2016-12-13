"""from __future__ import division
from matplotlib import pyplot as plt
import numpy as np
import math"""

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

    #Return generated histogram
    return hist


#Optimal threshold calculation function, using otsu's method
def calculateThresholds(image):
    #Generate histogram
    hist = generateHistogram(image)

    #Create dictionary for between class variances
    bc_variances = {}

    #Test all possible thresholds
    for threshold in range(1,256):
        #Split dictionary above/below threshold
        below_thres,above_thres = splitDictionary(hist,threshold)
        #Total number of pixels in image
        total = image.shape[0] * image.shape[1]

        #Calculate background weight and mean
        background_total = 0
        background_mean_total = 0
        for key, value in below_thres.items():
            background_total += value
            background_mean_total += key*value

        if total != 0:
            background_weight = background_total / total
        else:
            background_weight = 0

        if background_total != 0:
            background_mean = background_mean_total / background_total
        else:
            background_mean = 0

        #Calculate foreground weight and mean
        foreground_total = 0
        foreground_mean_total = 0
        for key, value in above_thres.items():
            foreground_total += value
            foreground_mean_total += key*value

        if total != 0:
            foreground_weight = foreground_total / total
        else:
            foreground_weight = 0

        if foreground_total != 0:
            foreground_mean = foreground_mean_total / foreground_total
        else:
            foreground_mean = 0

        #Calculate between class variance for current threshold
        between_class_variance = background_weight * foreground_weight * (
                background_mean - foreground_mean)**2
        bc_variances[threshold] = between_class_variance

    #Find largest value in bc_variances, and store the threshold
    optimal_thres = max(bc_variances,key=bc_variances.get)
    choice = str(input('Show threshold selection plot? (y/n)'))
    if choice == 'y':
        a=range(1,256)
        values = [bc_variances[i] for i in range(1,256)]
        plt.plot(a,values)
        plt.show()
    print('Optimal threshold: ',optimal_thres)
    choice = str(input('Show histogram? (y/n)'))
    if choice == 'y':
        plt.bar(hist.keys(),hist.values(),1)
        plt.plot((optimal_thres,optimal_thres),(0,max(hist.values())),'r-')
        plt.show()

    #Return threshold with optimal between class variance
    return optimal_thres

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

#Interface function, to interact with main program
def threshold(image,magnitude,suppressedImage, lowThreshRatio,  highThreshRatio):
    #Calculate main threshold
    #highThreshRatio = 0.275 #Ratio OF max gradient magnitude
    #lowThreshRatio = 0.25 #Ratio OF highThreshRatio

    #t = calculateThresholds(suppressedImage)
    #Threshold the image using high and low threshold
    highThresh = highThreshRatio*np.max(magnitude)
    lowThresh = lowThreshRatio*highThresh

    #Threshold that shit
    output, strongEdgesQueue = threshold_image(suppressedImage,lowThresh,highThresh)

    #Return thresholded image
    return output, strongEdgesQueue
