import numpy as np

from scipy.ndimage import variance
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import laplace
from skimage.transform import resize

# Load image
path1 = "./dset/image 1.png"
path2 = "./dset/image 2.png"
img1 = io.imread(path1)
img2 = io.imread(path2)

# Grayscale image
img1 = rgb2gray(img1)
img2 = rgb2gray(img2)

# Edge detection
edge_laplace1 = laplace(img1, ksize=10)
edge_laplace2 = laplace(img2, ksize=10)

# Print output
print("Sharp:")
print(f"Variance: {variance(edge_laplace1)}")
print(f"Maximum : {np.amax(edge_laplace1)}")
print("\nBlurry:")
print(f"Variance: {variance(edge_laplace2)}")
print(f"Maximum : {np.amax(edge_laplace2)}")

import cv2

loaded_image = cv2.imread(path1)
cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()

print("\nBlur: " + str(image_variance))

loaded_image = cv2.imread(path2)
cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()

print("Blur: " + str(image_variance))
