# Spectra
Spectra is an image processing algorithm designed to detect scenes, similarity, and blur in sequentially ordered images and give suggestions to the user to review and perhaps delete these files that are deemed to be dispensable.

Automatic organization and labeling of images based on image attributes coming soon.

Supports JPG, JPEG, and PNG file formats.

## Install Dependencies

Please run the [install.sh](https://github.com/nalinahuja22/spectra/blob/master/install.sh) setup script included within the repository to install all the dependencies required by Spectra. You **must** have a version of **pip** installed on your machine to successfully install the required dependencies.   

The script will install cv2 and imagehash to your global python modules.

## Usage
```
#For Python 2 Users
python analyze.py $IMG_PATH

#For Python 3 Users
python3 analyze.py $IMG_PATH
```
