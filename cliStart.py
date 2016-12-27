import sys
from PIL import Image as im
import numpy as np
sys.path.insert(0, '/home/cwp')
import canny

def showSaveChoice(image, message=None):
    if message:
        print(message)
    while True:
        choice = str(input('Enter D to display, S to save, or press enter to skip'))
        if choice == 'D':
            display(image)
            break
        elif choice == 'S':
            save(image)
            break
        elif choice == '':
            break
        else:
            print('Invalid choice')

def getSigma():
    while True:
        try:
            sigma = float(input('Enter gaussian blur standard deviation: '))
            if sigma < 0:
                print('Invalid standard deviation: must be larger than 0')
                continue
            if sigma > 5:
                print('Invalid standard deviation: must be less than 5')
                continue
            return sigma
        except ValueError:
            print('Invalid standard deviation: must be float')

def getWidth():
    while True:
        try:
            width = int(input('Enter gaussian kernel radius: '))
            if width % 2 != 1:
                print('Kernel radius must be odd')
                continue
            if width < 3:
                print('Kernel radius must be at least 3')
                continue
            if width > 11:
                print('Kernel radius must be at most 11')
                continue
            return width
        except ValueError:
            print('Invalid kernel radius: must be integer')

def save(image):
    while True:
        try:
            filepath = str(input('Enter filepath to save: '))
            im.fromarray(image).save(filepath)
        except:
            print('Error whilst saving')

def display(image):
    while True:
        try:
            im.fromarray(image).show()
            break
        except:
            print('Error opening image')

def getThresholds():
    while True:
        try:
            choice = str(input('Enter M to manually choose threshold ratios, or A to automatically generate: '))
            if choice == 'A':
                return True, None, None
            elif choice == 'M':
                highThreshRatio = float(input('Enter high threshold ratio: '))
                lowThreshRatio = float(input('Enter low threshold ratio: '))
                return False, highThreshRatio, lowThreshRatio
            else:
                print('Invalid choice')
        except ValueError:
            print('Threshold ratios must be floats')

while True:
    try:
        filepath = str(input('Enter filepath to image: '))
        I = canny.Image(np.asarray(im.open(filepath).convert('L')))
        print('Image loaded from '+filepath)
        break
    except:
        print('Error loading image')

sigma = getSigma()
width = getWidth()
print('Gaussian now processing')
I.gaussian_(sigma, width)
print('Gaussian blur complete')
showSaveChoice(I.gblur)

print('Sobel filter now processing')
I.sobel_()
print('Sobel filter complete')
sobel = {'Sobel magnitude': I.smagnitude, 'Sobel direction':I.sdirection, 'Sobel vertical gradient':I.svgradient, 'Sobel horizontal gradient':I.shgradient}
for msg,image in sobel.items():
    showSaveChoice(image, msg)

print('Non maximum suppression now processing')
I.nms_()
print('Non maximum suppression complete')
showSaveChoice(I.suppressed)

auto, lowThreshRatio, highThreshRatio = getThresholdChoice()
print('Thresholding now processing')
if auto == True:
    I.threshold_(True)
else:
    I.threshold_(False, lowThreshRatio, highThreshRatio)
print('Thresholding complete')
showSaveChoice(I.thresholded)

print('Hysteresis now processing')
I.hysteresis_()
print('Hysteresis complete')
showSaveChoice(I.final)
