import cv2
from PIL import Image

img = cv2.imread('./IMG_0294.JPG')
new_image = cv2.convertScaleAbs(img, alpha = 4, beta = 10)

cv2.imwrite("./image_processeda4b10.jpg", new_image)

#alpha is brightness, beta is contrast

# ./IMG_0294.JPG - Brightness: 54.17938218467793 - Blur: 7.460262007280507
# ./image_processeda1b35.jpg - Brightness: 89.16787481111754 - Blur: 8.960062074624657
# ./image_processeda2b35.jpg - Brightness: 135.8278435182506 - Blur: 25.251215723878964
# ./image_processeda3b35.jpg - Brightness: 151.50152786038595 - Blur: 37.4113330814625
# ./image_processeda4b10.jpg - Brightness: 145.62167608176512 - Blur: 56.2209674686685
# ./image_processeda4b35.jpg - Brightness: 159.5903022811464 - Blur: 51.01872726160844
# ./image_processeda4b50.jpg - Brightness: 167.8679132797318 - Blur: 48.14078853028855
