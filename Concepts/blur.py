import numpy as np
import os

from scipy.ndimage import variance
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import laplace

path = os.path.normpath("./dset")

edge_laplace1 = None

variancelist = []
maximum = []
label = []

for file in os.listdir(path):
    if file.endswith((".jpg", ".png", ".jpeg", ".JPG", ".JPEG", ".PNG")):
        # Load image
        img1 = io.imread(os.path.join(path, file))

        # Grayscale image
        img1 = rgb2gray(img1)

        # Print output
        variancelist.append(variance(laplace(img1, ksize=10)))
        maximum.append(np.amax(laplace(img1, ksize=10)))
        label.append(file)

print(variancelist)
print(maximum)
print(label)
