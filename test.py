import numpy as np
from PIL import Image as im
import canny

canny.fullCanny(np.asarray(im.open('/home/cwp/NEA2/test.png').convert('L')))
