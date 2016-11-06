from __future__ import division
from matplotlib import pyplot as plt
import numpy as np
import math

def splitDictionary(dictionary,threshold):
    low_dict = {}
    high_dict = {}
    for key, value in dictionary.items():
        if value < threshold:
            low_dict[key] = value
        else:
            high_dict[key] = value
    return low_dict, high_dict

def generateHistogram(image):
    hist={}
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            val = math.floor(image[i][j])
            if val in hist:
                hist[val] += 1
            else:
                hist[val] = 1
    return hist

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
    a=range(1,256)
    values = [bc_variances[i] for i in range(1,256)]
    plt.plot(a,values)
    plt.show()
    print(optimal_thres)
    #Return threshold with optimal between class variance
    #plt.bar(hist.keys(),hist.values(),1)
    #plt.plot((optimal_thres,optimal_thres),(0,max(hist.values())),'r-')
    #plt.show()
    return optimal_thres

def threshold_image(image,low,high):
    output = np.zeros(image.shape)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] >= high:
                output[i][j] = 255
            elif image[i][j] < low:
                output[i][j] = 0
            else:
                output[i][j] = 128
    return output

def threshold(image,suppressedImage):
    t = 120 # calculateThresholds(suppressedImage)
    output = threshold_image(suppressedImage,0.05*t,0.3*t)
    return output
