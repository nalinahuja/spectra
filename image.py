#Developed by Nalin Ahuja, nalinahuja22

import os
import cv2
import file
import imagehash

from PIL import Image, ImageStat

_precision = 1.75

class process:
    def __init__(self, args):
        #Initialize Default Values
        self.image_path = file.normalize(args[0])
        assert(self.image_path != None)

        #Define Image Data Lists
        self.image_list = None
        assert(self.image_list == None)
        self.image_hashes = None
        assert(self.image_hashes == None)
        self.hash_diffs = None
        assert(self.hash_diffs == None)
        self.image_scenes = None
        assert(self.image_scenes == None)
        self.image_duplicates = None
        assert(self.image_duplicates == None)

        #Image Attribute Values
        self.scene_threshold = 40 if args[1] == None else args[1]
        self.dupli_threshold = 15 if args[2] == None else args[2]
        self.sharp_threshold = 15 if args[3] == None else args[3]

        #Get Directory Contents
        self._get_dir_contents(self.image_path)

        #Calculate Image Data
        self._calculate_image_hashes()
        self._calculate_hash_differences()

        #Analyze Image Data
        self._detect_scenes()
        # self._detect_duplicates()

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
        if (self.image_hashes != None):
            #Initialize Diff List
            self.hash_diffs = []

            #Calculate Hash Differences
            for i in range(len(self.image_hashes) - 1):
                self.hash_diffs.append((self.image_hashes[i + 1] - self.image_hashes[i]) * _precision)
        else:
            print("ERROR: No Image Hashes Found to Process")

    #End Processing Functions-------------------------------------------------------------------------------------------------------------------------

    def _detect_scenes(self):
        if (self.hash_diffs != None):
            #Initalize Scene List
            self.image_scenes = []

            #Initialize Scene
            scene = []

            #Inialize Image Counter
            curr_image = 0;

            #Determine Scenes
            for diff in self.hash_diffs:
                if (diff >= self.scene_threshold):
                    if (not(self.image_list[curr_image] in scene)):
                        scene.append(self.image_list[curr_image])
                    self.image_scenes.append(scene)
                    scene = []
                else:
                    if (not(self.image_list[curr_image] in scene)):
                        scene.append(self.image_list[curr_image])
                    if (not(self.image_list[curr_image + 1] in scene)):
                        scene.append(self.image_list[curr_image + 1])

                curr_image += 1

            if (not(self.image_list[curr_image] in scene) and curr_image != len(self.image_list)):
                scene.append(self.image_list[curr_image])
            if (len(scene) > 0):
                self.image_scenes.append(scene)
        else:
            print("ERROR: No Image Differences Found to Process")

    #End Scene Function-------------------------------------------------------------------------------------------------------------------------------

    def _detect_duplicates(self):
        if (self.hash_diffs != None):
            #Initialize Duplicate Array
            self.image_duplicates = []

            #Initialize Scene Array
            duplicates = []

            #Initialize Image Counter
            curr_image = 0

            print(self.hash_diffs)

            #Determine Duplicates
            for diff in self.hash_diffs:
                if (diff <= self.dupli_threshold):
                    if (not(self.image_list[curr_image] in duplicates)):
                        duplicates.append(self.image_list[curr_image])
                    if (not(self.image_list[curr_image + 1] in duplicates)):
                        duplicates.append(self.image_list[curr_image + 1])
                else:
                    if (len(duplicates) > 0):
                        self.image_duplicates.append(duplicates)
                        duplicates = []

                curr_image += 1

            if (not(self.image_list[curr_image] in duplicates) and curr_image != len(self.image_list)):
                duplicates.append(self.image_list[curr_image])
            if (len(duplicates) > 0):
                self.image_scenes.append(duplicates)
        else:
            print("ERROR: No Image Differences Found to Process")

    #End Duplicate Function---------------------------------------------------------------------------------------------------------------------------

    # def detect_blur(self, threshold = None):
    #     #Process Set Arguments
    #     if (not(threshold is None)):
    #         self.blur_threshold = threshold
    #
    #     #Initalize Blurred Images Array
    #     blurred_images = []
    #
    #     for image in self.image_list:
    #         loaded_image = cv2.imread(image)
    #         cv_gray_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
    #         image_variance = cv2.Laplacian(cv_gray_image, cv2.CV_64F).var()
    #
    #         print(image + " : " + str(image_variance))
    #
    #         # im = Image.open(image).convert('L')
    #         # stat = ImageStat.Stat(im)
    #         # stat.mean[0]
    #
    #         # if (image_variance < self.blur_threshold):
    #         # blurred_images.append(image)
    #
    #     #Return Blurred Images Array
    #     return blurred_images

    #End Blur Function--------------------------------------------------------------------------------------------------------------------------------

    def organize_images(self):
        if (self.image_scenes != None):
            #Iterate over image_scenes array
            for i in range(len(self.image_scenes)):
                file.mkdir(file.formDir([self.image_path, file._scene.format(i + 1)]))
                for j in range(len(self.image_scenes[i])):
                    try:
                        #Get Image Directory Contents
                        image_directory = self.image_scenes[i][j].split(file._fslash)

                        #Generate Source and Destination Paths
                        src = file.normalize(self.image_scenes[i][j])
                        dest = file.normalize(file.formDir([image_directory[0], file._scene.format(i + 1), image_directory[1]]))

                        #Move Files to Scene Folders
                        file.move(src, dest)
                    except:
                        pass
        else:
            print("ERROR: No Scenes Found to Analyze")

    #End User Functions-------------------------------------------------------------------------------------------------------------------------------
