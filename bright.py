import os
import cv2
from PIL import Image
from PIL import ImageStat

def get_dir_contents(path):
    #Initialize Image List
    image_list = []

    path = os.path.normpath(path)

    #Store Image Paths
    for file in os.listdir(path):
        if file.endswith((".jpg", ".png", ".jpeg", ".tiff", ".JPG", ".JPEG", ".PNG", ".TIFF")):
            image_list.append(os.path.join(path, file))

    #Sort Image Paths by Number
    image_list.sort()

    return image_list

def brightness(im_file):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]

if __name__ == "__main__":
    image_path = "./Images"

    for image in get_dir_contents(image_path):
        loaded_image = cv2.imread(image)
        cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
        image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()

        print(str(image) + " - Brightness: " + str(brightness(image)) + " - Blur: " + str(image_variance))
