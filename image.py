#Developed by Nalin Ahuja, nalinahuja22

import os
import file

import cv2
import imagehash

from PIL import Image, ImageStat

_precision = 1.75

class process:
    def __init__(self, args):
        #Process Arguments
        self.image_path = file.normalize(args[0])
        self.scene_threshold = 45 if args[1] == None else args[1]
        self.dupli_threshold = 20 if args[2] == None else args[2]
        self.sharp_threshold = 15 if args[3] == None else args[3]

        #Define Image Data Lists
        self.image_list = None
        self.hash_diffs = None

        #Define Processed Image Data
        self.image_blur = None
        self.image_scenes = None
        self.image_duplicates = None

        #Fetch Directory Contents
        self._get_dir_contents()

        #Calculate Image Data
        self._calculate_hash_differences()

        #Analyze Image Data
        self._detect_scenes()
        self._detect_duplicates()

        # self._detect_blur()

        #Cleanup Image Directory
        self.organize_directory()

    #End Object Constructor----------------------------------------------------------------------------------------------------------------------------------------

    def _get_dir_contents(self):
        if (self.image_path != None):
            #Set Global Scope
            global file

            #Declare Subroutine
            print("Loaded Images From ./{}".format(self.image_path))

            #Initialize Image Paths List
            self.image_list = []

            #Normalize and Store Image Paths
            for path, subdirs, files in os.walk(self.image_path):
                for file_name in files:
                    if (file_name.endswith((".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"))):
                        image_data = {'dir': os.path.realpath(path), 'file_name': file_name, 'path': os.path.join(path, file_name)}
                        if (self.image_path != image_data['dir']):
                            file.move(image_data['path'], os.path.realpath("{}/{}".format(self.image_path, image_data['file_name'])))
                        self.image_list.append(os.path.join("./{}".format(self.image_path), image_data['file_name']))

            #Delete Empty Directories
            for file in os.listdir(self.image_path):
                normpath = "{}/{}".format(self.image_path, file)
                if (os.path.isdir(normpath)):
                    try:
                        os.rmdir(normpath)
                    except OSError:
                        pass

            #Sort Image Paths in Lexicographical Order
            self.image_list.sort()
        else:
            print("ERROR: Image Path is Invalid")

    #End Util Fucntions---------------------------------------------------------------------------------------------------------------------------------------------

    def _calculate_hash_differences(self):
        if (self.image_list != None):
            #Initialize Hash List
            image_hashes = []

            #Declare Process Counter
            cnt = 0

            #Calculate Hash Values
            for image in self.image_list:
                print("Processing Images - {}%".format(int(cnt * 100 / float(len(self.image_list)))), end="\r")
                image_hashes.append(imagehash.average_hash(Image.open(image)))
                cnt += 1

            #Declare Subroutine
            print("Processed Images From ./{}".format(self.image_path))

            #Initialize Diff Listx
            self.hash_diffs = []

            #Calculate Hash Differences
            for i in range(len(image_hashes) - 1):
                self.hash_diffs.append((image_hashes[i + 1] - image_hashes[i]) * _precision)

        else:
            print("ERROR: No Images Found to Process")

    #End Processing Functions---------------------------------------------------------------------------------------------------------------------------------------

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

            if (curr_image < len(self.image_list) and not(self.image_list[curr_image] in scene)):
                scene.append(self.image_list[curr_image])
            if (len(scene) > 0):
                self.image_scenes.append(scene)
        else:
            print("ERROR: No Image Differences Found to Process")

    #End Scene Function---------------------------------------------------------------------------------------------------------------------------------------------

    def _detect_duplicates(self):
        if (self.hash_diffs != None):
            #Initialize Duplicate Array
            self.image_duplicates = []

            #Initialize Scene Array
            duplicates = []

            #Initialize Image Counter
            curr_image = 0

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
                self.image_duplicates.append(duplicates)
        else:
            print("ERROR: No Image Differences Found to Process")

    #End Duplicate Function----------------------------------------------------------------------------------------------------------------------------------------

    # def detect_blur(self):
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

    #End Blur Function---------------------------------------------------------------------------------------------------------------------------------------------

    def organize_directory(self):
        if (self.image_scenes != None):
            #Declare Subroutine
            print("Organizing Images In {}".format(self.image_path))

            #Iterate over image_scenes array
            for i in range(len(self.image_scenes)):
                os.mkdir(file.formDir([self.image_path, file._scene.format(i + 1)]))
                for j in range(len(self.image_scenes[i])):
                    try:
                        #Get Image Directory Contents
                        image_directory = self.image_scenes[i][j].split(file._fslash)

                        #Generate Source and Destination Paths
                        src = file.normalize(self.image_scenes[i][j])
                        dest = file.normalize(file.formDir([image_directory[0], file._scene.format(i + 1), image_directory[1]]))

                        #Move Files to Scene Folders
                        file.move(src, dest)
                    except FileNotFoundError:
                        pass
        else:
            print("ERROR: No Scenes Found to Analyze")

    #End User Functions--------------------------------------------------------------------------------------------------------------------------------------------
