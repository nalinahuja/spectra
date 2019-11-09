#Developed by Nalin Ahuja, nalinahuja22

#!/bin/bash

read -p "Please Select Your Version of Python [2.x, 3.x]: " version

if [ ! $version == 2.x ] && [ ! $version == 3.x ]
then
  echo -e "\nImproper Python Version, Installation Aborted!"
  exit 1
fi

if [ $version == 2.x ]
then
  echo -e "\nInstalling Python Dependencies..."
  pip install cv2
  pip install imagehash
elif [ $version == 3.x ]
then
  echo -e "\nInstalling Python3 Dependencies..."
  pip3 install cv2
  pip3 install imagehash
fi

echo -e "\nSuccessfully Installed Imagehash and cv2!"
