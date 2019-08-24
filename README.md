# Similarity
Similarity is an image processing algorithm to detect sequentially ordered duplicate images with scene detection as well as out of order blurred images. Is able to discern augmentation, color correction, and shallow depth of field as unique qualities to images.

Supports JPG, PNG, and CR2 file formats.

Updates to come: Automatic organization of images based on apparent scene, blur, and similarity.

## Install Dependencies

```
#For Python 2 Users
pip install cv2
pip install imagehash

#For Python 3 Users
pip3 install cv2
pip3 install imagehash
```

## Usage

```
#For Python 2 Users
python main.py DIR

#For Python 3 Users
python3 main.py DIR
```
