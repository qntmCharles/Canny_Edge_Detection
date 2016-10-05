import numpy as np
import math
import matplotlib.pyplot as plt

def plot(array):
    to_plot = [((item*(180/(2*math.pi)))+180)/360 for item in array]
    plt.imshow(array, cmap='gist_rainbow', interpolation='nearest')
    plt.show()
