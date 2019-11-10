#Developed by Nalin Ahuja, nalinahuja22

import os
import cv2
import imagehash
import numpy as np

from skimage import io
from scipy.ndimage import variance
from skimage.color import rgb2gray
from skimage.filters import laplace
from PIL import Image, ImageStat

#End Imports--------------------------------------------------------------------------------------------------------------------------------------------------------

_fslash = "/"
_scene = "Scene {}"

def move(src, dest):
    os.rename(src, dest)

def normalize(path):
    return os.path.normpath(path)

def formDir(arr):
    dir = ""
    for path in arr:
        dir += str(path) + _fslash
    return normalize(dir[:-1])

#End File Management Functions--------------------------------------------------------------------------------------------------------------------------------------

_precision = 1.75
_max_threshold = 0.5
_var_threshold = 0.0005

class process:
    def __init__(self, args):
        #Process Arguments
        self.image_path = normalize(args[0])
        self.scene_threshold = 45 if args[1] == None else args[1]
        self.dupli_threshold = 20 if args[2] == None else args[2]
        self.sharp_threshold = 15 if args[3] == None else args[3]

        #Define Image Data Lists
        self.image_list = None
        self.hash_diffs = None

        #Define Processed Image Data
        self.image_scenes = None
        self.blurred_images = None
        self.image_duplicates = None

        #Fetch Directory Contents
        self._get_dir_contents()

        #Calculate Image Data
        self._process_images()

        #Analyze Image Data
        self._detect_scenes()
        self._detect_duplicates()

        #Cleanup Image Directory
        self._organize_directory()

    #End Object Constructor-----------------------------------------------------------------------------------------------------------------------------------------

    def _get_dir_contents(self):
        if (self.image_path != None):
            #Initialize Image Paths List
            self.image_list = []

            #Declare Process Counter
            cnt = 0

            #Normalize and Store Image Paths
            for path, subdirs, files in os.walk(self.image_path):
                for file_name in files:
                    if (file_name.endswith((".jpg", ".jpeg", ".png", ".tiff", ".JPG", ".JPEG", ".PNG", ".TIFF"))):
                        image_data = {'dir': os.path.realpath(path), 'file_name': file_name, 'path': os.path.join(path, file_name)}
                        if (self.image_path != image_data['dir']):
                            move(image_data['path'], os.path.realpath("{}/{}".format(self.image_path, image_data['file_name'])))
                        self.image_list.append(os.path.join("./{}".format(self.image_path), image_data['file_name']))
                        print("Loaded {} Images - ./{}".format(cnt, self.image_path), end="\r")
                        cnt += 1

            #Delete Empty Directories
            for file in os.listdir(self.image_path):
                normpath = "{}/{}".format(self.image_path, file)
                if (os.path.isdir(normpath)):
                    try:
                        os.rmdir(normpath)
                    except OSError:
                        pass

            #Declare Subroutine
            print("Loaded All Images - ./{}".format(self.image_path))

            #Sort Image Paths in Lexicographical Order
            self.image_list.sort()
        else:
            print("ERROR: Image Path is Invalid")

    #End Util Fucntions---------------------------------------------------------------------------------------------------------------------------------------------

    def _process_images(self):
        if (self.image_list != None):
            #Initialize Hash List
            image_hashes = []

            #Declare Process Counter
            cnt = 0

            #Calculate Hash Values
            for image in self.image_list:
                print("Processing Images - {}%".format(int(cnt * 100 / float(len(self.image_list) * 2))), end="\r")
                image_hashes.append(imagehash.average_hash(Image.open(image)))
                cnt += 1

            #End Image Hash-----------------------------------------------------------------------------------------------------------------------------------------

            #Initialize Diff List
            self.hash_diffs = []

            #Calculate Hash Differences
            for i in range(len(image_hashes) - 1):
                self.hash_diffs.append((image_hashes[i + 1] - image_hashes[i]) * _precision)

            #End Hash Diff Computation------------------------------------------------------------------------------------------------------------------------------

            #Initalize Blurred Images Array
            self.blurred_images = []

            #Iterate Over Image List
            for image in self.image_list:
                #Load Image
                loaded_image = io.imread(image)

                #Grayscale Image
                loaded_image = rgb2gray(loaded_image)

                #Determine Edges
                laplace_data = laplace(loaded_image, ksize=10)
                variance_score = variance(laplace_data)
                maximum_score = np.amax(laplace_data)

                #Accordinly Categorize Images
                if (variance_score < _var_threshold and maximum_score < _max_threshold):
                    self.blurred_images.append(image)

                #Declare Subroutine
                print("Processing Images - {}%".format(int(cnt * 100 / float(len(self.image_list) * 2))), end="\r")
                cnt += 1

            #Declare Subroutine
            print("Processed All Images       ")
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

    #End Duplicate Function-----------------------------------------------------------------------------------------------------------------------------------------

    def _organize_directory(self):
        if (self.image_scenes != None):
            #Iterate over image_scenes array
            for i in range(len(self.image_scenes)):
                os.mkdir(formDir([self.image_path, _scene.format(i + 1)]))
                for j in range(len(self.image_scenes[i])):
                    try:
                        #Get Image Directory Contents
                        image_scene = self.image_scenes[i][j]
                        image_directory = image_scene.split(_fslash)

                        #Generate Source and Destination Paths
                        src = normalize(image_scene)
                        dest = normalize(formDir([image_scene[0:image_scene.rfind('/')], _scene.format(i + 1), image_directory[2]]))

                        #Move Files to Scene Folders
                        move(src, dest)
                    except FileNotFoundError:
                        pass

            #Declare Subroutine
            print("Organized All Images       ")
        else:
            print("ERROR: No Scenes Found to Analyze")

    #End Organize Function------------------------------------------------------------------------------------------------------------------------------------------

#End Process Class--------------------------------------------------------------------------------------------------------------------------------------------------
