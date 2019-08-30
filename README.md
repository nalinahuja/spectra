# Spectra
Spectra is an image processing algorithm designed to detect scenes, similarity, and blur in sequentially ordered images and give suggestions to the user to review and perhaps delete these files that are deemed to be dispensable.

Automatic organization and labeling of images based on image attributes coming soon.

Supports JPG, JPEG, and PNG file formats.

## Install Dependencies

Please either run the below commands or run the [install.sh](https://github.com/nalinahuja22/spectra/blob/master/install.sh) script included within the repository.

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
python analyze.py $PATH

#For Python 3 Users
python3 analyze.py $PATH
```
