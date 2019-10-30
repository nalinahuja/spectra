#Developed by Nalin Ahuja, nalinahuja22

import os
import cv2
import imagehash

from PIL import Image, ImageStat

_precision = 1.75

class process:
    def __init__(self, args):
        #Initialize Default Values
        self.image_path = os.path.normpath(args[0])
        assert(self.image_path != None)

        #Define Image Data Lists
        self.image_list = None
        assert(self.image_list == None)
        self.image_hashes = None
        assert(self.image_hashes == None)

        #Image Attribute Values
        self.scene_threshold = 15 if args[1] == None else args[1]
        self.dupli_threshold = 15 if args[2] == None else args[2]
        self.sharp_threshold = 15 if args[3] == None else args[3]

        #Get Image Path Contents
        self._get_dir_contents(self.image_path)

        #Calculate Image Data
        self._calculate_image_hashes()
        self._calculate_hash_differences()

    #End Object Constructor---------------------------------------------------------------------------------------------------------------------------

    def _get_dir_contents(self, path):
        #Initialize Image List
        self.image_list = []

        #Store Image Paths
        for file in os.listdir(path):
            if file.endswith((".jpg", ".png", ".jpeg", ".JPG", ".JPEG", ".PNG")):
                self.image_list.append(os.path.join(path, file))

        #Sort Image Paths in Lexicographical Order
        self.image_list.sort()

    #End Util Fucntions-------------------------------------------------------------------------------------------------------------------------------

    def _calculate_image_hashes(self):
        if (self.image_list != None):
            #Initialize Hash List
            self.image_hashes = []

            #Calculate Hash Values
            for image in self.image_list:
                self.image_hashes.append(imagehash.average_hash(Image.open(image)))
        else:
            print("ERROR: No Images Found to Process")

    def _calculate_hash_differences(self):
        if (self.hash_diffs != None):
            #Initialize Diff List
            self.hash_diffs = []

            #Calculate Hash Differences
            for i in range(len(self.image_hashes) - 1):
                self.hash_diffs.append((self.image_hashes[i + 1] - self.image_hashes[i]) * _precision)
        else:
            print("ERROR: No Image Differences Found to Process")

    #End Processing Functions-------------------------------------------------------------------------------------------------------------------------

    def detect_scenes(self):
        if (self.hash_diffs != None):
            #Initialize Scene Count
            scenes = 1

            #Determine Scenes
            for diff in self.hash_diffs:
                if (diff >= self.scene_threshold):
                    scenes += 1

            #Return Scene Count
        return scenes if (len(self.image_list) > 0) else 0




























    def detect_duplicates(self, threshold = None):
        #Process Set Arguments
        if (not(threshold is None)):
            self.duplicate_threshold = threshold

        #Initialize Duplicate Array
        duplicates = []

        #Initialize Scene Array
        scene = []

        #Determine Duplicates
        for i in range(len(self.hash_diffs)):
            if (self.hash_diffs[i] <= self.duplicate_threshold):
                if (not(self.image_list[i] in scene)):
                    scene.append(self.image_list[i])
                if (not(self.image_list[i + 1] in scene)):
                    scene.append(self.image_list[i + 1])
            elif (len(scene) > 1):
                duplicates.append(scene)
                scene = []

        if (len(scene) != 0):
            duplicates.append(scene)

        #Return Duplicate Array
        return duplicates

    def detect_blur(self, threshold = None):
        #Process Set Arguments
        if (not(threshold is None)):
            self.blur_threshold = threshold

        #Initalize Blurred Images Array
        blurred_images = []

        for image in self.image_list:
            loaded_image = cv2.imread(image)
            cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
            image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()

            print(image + " : " + str(image_variance))

            # im = Image.open(image).convert('L')
            # stat = ImageStat.Stat(im)
            # stat.mean[0]

            # if (image_variance < self.blur_threshold):
            # blurred_images.append(image)

        #Return Blurred Images Array
        return blurred_images

    #End Detection Functions--------------------------------------------------------------------------------------------------------------------------
