from PIL import Image as im
import numpy as np
import math
import decimal
decimal.getcontext().prec = 15
#Do I need that? ^^ Does it actually make a difference...

from .imageClass import Image
from .gaussian import gaussian
from .sobel import sobel
from .convolution import convolution
from .threshold import thresholdInterface
from .hysteresis import hysteresis

print('canny initialised')
