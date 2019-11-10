import cv2
from PIL import Image, ImageStat

def brightness(im_file):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]

if __name__ == "__main__":
    image = "./../Images/alt/IMG_0340.JPG"
    loaded_image = cv2.imread(image)

    cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
    image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()
    print("BEFORE: " + str(image) + " - Brightness: " + str(brightness(image)) + " - Blur: " + str(image_variance))

    new_image = cv2.convertScaleAbs(loaded_image, alpha = 1, beta = -100)

    cv2.imwrite("./edges.jpg", cv2.Laplacian(cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY), cv2.CV_64F))
    cv2.imwrite("./new_image.jpg", new_image)

    image = "./new_image.jpg"
    loaded_image = cv2.imread(image)

    cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
    image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()
    print("AFTER: " + str(image) + " - Brightness: " + str(brightness(image)) + " - Blur: " + str(image_variance))

#alpha is brightness, beta is contrast

# ./IMG_0294.JPG - Brightness: 54.17938218467793 - Blur: 7.460262007280507
# ./image_processeda1b35.jpg - Brightness: 89.16787481111754 - Blur: 8.960062074624657
# ./image_processeda2b35.jpg - Brightness: 135.8278435182506 - Blur: 25.251215723878964
# ./image_processeda3b35.jpg - Brightness: 151.50152786038595 - Blur: 37.4113330814625
# ./image_processeda4b10.jpg - Brightness: 145.62167608176512 - Blur: 56.2209674686685
# ./image_processeda4b35.jpg - Brightness: 159.5903022811464 - Blur: 51.01872726160844
# ./image_processeda4b50.jpg - Brightness: 167.8679132797318 - Blur: 48.14078853028855

# BEFORE: ./test.png - Brightness: 110.00176775359725 - Blur: 3.8364565832491215
# AFTER: ./new_image.jpg - Brightness: 218.32619953110458 - Blur: 17.39530490706806
