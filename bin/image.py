#Developed by Nalin Ahuja, nalinahuja22

import os
import sys
import cv2
import util
import shutil
import warnings
import imagehash
import numpy as np

from const import *
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import laplace
from scipy.ndimage import variance
from PIL import Image, ImageStat

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

def time_diff(image_a, image_b):
    # Set Return Value To Max
    min_delta = sys.maxsize

    try:
        # Open Images
        image_a = Image.open(image_a)
        image_b = Image.open(image_b)

        # Get EXIF Data From Images
        time_a = ((image_a._getexif()[306]).split(" ")[1]).split(":")
        time_b = ((image_b._getexif()[306]).split(" ")[1]).split(":")

        # Parse Time Data
        hour_a = int(time_a[0])
        hour_b = int(time_b[0])

        min_a = int(time_a[1])
        min_b = int(time_b[1])

        # Normalize Minute Values
        if ((min_b < min_a) and (hour_b > hour_a)):
            min_b += 60

        # Compute Time Delta
        min_delta = (min_b - min_a)
    except:
        pass

    # Return Time Delta
    return (min_delta)

def load_image_data(image_path):
    # Initialize Image Data Map
    image_data = {}

    # Parse Image Data File
    try:
        # Open File For Reading
        with open(util.form_path([image_path, DATA_FILE]), 'r') as file:
            file_data = file.readlines()
        file.close()

        # Error Check File Data
        if (util.empty(file_data)):
            return (None)

        # Iterate Over File Data
        for line in file_data:
            # Formatted Read
            line_data = line.split(COMMA)

            # Initialize New Data Object (Variance, Nmax, Rmsv, Lmod)
            image_data[line_data[0]] = data(vari = float(line_data[1]), nmax = float(line_data[2]), rmsv = float(line_data[3]), lmod = float(line_data[4]))
    except:
        # Create File If Read Error Occurs
        open(util.form_path([image_path, DATA_FILE]), 'w')

    # Return Image Data Map
    return (image_data)

# End Util Functions---------------------------------------------------------------------------------------------------------------------------------------------------

class data:
    def __init__(self, vari = None, nmax = None, rmsv = None, lmod = None):
        self.vari = vari
        self.nmax = nmax
        self.rmsv = rmsv
        self.lmod = lmod

# End Data Class-------------------------------------------------------------------------------------------------------------------------------------------------------

class analyze:
    def __init__(self, args):
        # Initalize Precisions
        self.precision = 1.75
        self.rms_threshold = 75
        self.del_threshold = 1.0
        self.max_threshold = 0.5
        self.var_threshold = 0.0005

        # Initialize Arguments
        self.image_path = util.normalize(args[0])
        self.scene_threshold = 30 if args[2] is None else args[2]
        self.dupli_threshold = 20 if args[3] is None else args[3]
        self.sharp_threshold = 100 if args[1] is None else args[1]

        # Adjust Precisions
        self.max_threshold *= (self.sharp_threshold / 100)
        self.var_threshold *= (self.sharp_threshold / 100)

        # Declare Image Data List
        self.image_list = None

        # Declare Image Data Lists
        self.hashes = None
        self.hash_diffs = None

        # Declare Image Result Lists
        self.scenes = None
        self.blurred = None
        self.duplicates = None

        # Collect Directory Contents
        self.collect_directory()

        # Calculate Image Data
        self.process_images()

        # Analyze Image Data
        self.detect_scenes()
        self.detect_duplicates()

        # Organize Directory Contents
        self.organize_directory()

    # End Object Constructor-------------------------------------------------------------------------------------------------------------------------------------------

    def collect_directory(self):
        # Initialize Process Counter
        curr = 0

        # Initialize Image Paths List
        self.image_list = []

        # Congregate Image Files
        for path, subdirs, files in os.walk(str(self.image_path)):
            for file in files:
                # Select Files With Supported File Types
                if (file.endswith((".jpg", ".jpeg", ".png", ".tiff", ".JPG", ".JPEG", ".PNG", ".TIFF"))):
                    # Create Local Image Data Map
                    image_data = {'dir': util.absolute(path), 'name': file, 'path': util.form_path([path, file])}

                    # Move File To Opened Path
                    if (self.image_path != image_data['dir']):
                        util.move(image_data['path'], util.absolute(util.form_path([self.image_path, image_data['name']])))

                    # Add File To Image List
                    self.image_list.append(util.form_path([self.image_path, image_data['name']]))

                    # Update Prompt
                    print("\rLoaded {} Images - {}".format(curr, self.image_path), end="")
                    curr += 1

        # Delete Empty Directories
        for file in os.listdir(str(self.image_path)):
            # Create Normalized Path
            dir_path = util.form_path([self.image_path, file])

            # Check Directory Existence
            if (util.exists(dir_path)):
                try:
                    # Remove Empty Directory
                    os.rmdir(dir_path)
                except OSError:
                    pass

        # Update Prompt
        print("\rLoaded All Images - {}".format(self.image_path))

        # Verify Image List Length
        if (util.empty(self.image_list)):
            util.perror("spectra: No images found")

        # Sort Image Paths in Lexicographical Order
        self.image_list.sort()

    def organize_directory(self):
        if (not(self.scenes is None) and not(util.empty(self.scenes))):
            # Iterate Over Scenes List
            for curr, scene in enumerate(self.scenes, 1):
                # Create Scene Folder
                util.mkdir(util.form_path([self.image_path, SCENE.format(curr)]))

                # Move Images To Scene Folder
                for image in scene:
                    try:
                        # Generate Source and Destination Paths
                        src = util.absolute(image)
                        dst = util.normalize(util.form_path([util.dirname(image), SCENE.format(curr), util.basename(image)]))

                        # Move Images To Scene Folder
                        util.move(src, dst)
                    except FileNotFoundError:
                        pass

            # Update Prompt
            print("Organized All Images             ")
        else:
            util.perror("ERROR: No Scenes Found to Analyze")

    # End Directory Fucntions------------------------------------------------------------------------------------------------------------------------------------------

    def detect_scenes(self):
        if (not(self.hash_diffs is None) and not(util.empty(self.hash_diffs))):
            # Initalize Scenes List
            self.scenes = []

            # Initialize Scene
            scene = [self.image_list[0]]

            # Determine Scenes
            for curr, diff in enumerate(self.hash_diffs, 1):
                # End Scene And Append To List
                if ((diff >= self.scene_threshold) and (time_diff(self.image_list[curr - 1], self.image_list[curr]) > self.del_threshold)):
                    self.scenes.append(scene)
                    scene = [self.image_list[curr]]
                else:
                    # Append Image To Scene
                    if (not(self.image_list[curr] in scene)):
                        scene.append(self.image_list[curr])

            # Append Final Scene
            if (not(util.empty(scene))):
                self.scenes.append(scene)
        else:
            util.perror("spectra: No image differences found to process")

    def detect_duplicates(self):
        if (not(self.hash_diffs is None) and not(util.empty(self.hash_diffs))):
            # Initialize Duplicates List
            self.duplicates = []

            # Initialize Group List
            duplicate_group = []

            # Determine Duplicates
            for curr, diff in enumerate(self.hash_diffs, 0):
                # Add Image Pair To Duplicate Group
                if (diff <= self.dupli_threshold):
                    if (not(self.image_list[curr] in duplicate_group)):
                        duplicate_group.append(self.image_list[curr])
                    if (not(self.image_list[curr + 1] in duplicate_group)):
                        duplicate_group.append(self.image_list[curr + 1])
                # Append Duplicate Group To List
                elif (len(duplicate_group) > 1):
                    self.duplicates.append(duplicate_group)
                    duplicate_group = []

            # Append Final Duplicate Group
            if (len(duplicate_group) > 1):
                self.duplicates.append(duplicate_group)
        else:
            util.perror("spectra: No image differences found to process")

    # End Detection Functions------------------------------------------------------------------------------------------------------------------------------------------

    def process_images(self):
        if (not(self.image_list is None) and not(util.empty(self.image_list))):
            # Initialize Process Counter
            curr = 0

            # Initialize Hash List
            self.hashes = []

            # Initalize Blurred Array
            self.blurred = []

            # Load Image Data Map
            image_data = load_image_data(self.image_path)

            # Error Check Image Data Map
            if (image_data is None):
                image_data = {}

            # Calculate Hash Values
            for image in self.image_list:
                # Create Data Object
                if (not(image in image_data)):
                    image_data[image] = data(lmod = util.get_lmod(image))

                # Calculate Imagehash
                self.hashes.append(imagehash.average_hash(Image.open(image)))

                # End Imagehash Calculation----------------------------------------------------------------------------------------------------------------------------

                # Store Image Name
                input_image = image

                # Store Recent Modification Time
                curr_lmod = util.get_lmod(image)

                # Calculate Blur Coefficient
                if ((image_data[image].vari is None) or (image_data[image].nmax is None) or
                    (image_data[image].rmsv is None) or (image_data[image].lmod < curr_lmod)):
                    # Compute RMS Value
                    loaded_image = Image.open(image).convert('L')
                    image_stats = ImageStat.Stat(loaded_image)
                    image_rms = image_stats.rms[0]

                    # Determine RMS Deficiency
                    if (image_rms < self.rms_threshold):
                        # Create Cache Folder
                        try:
                            util.mkdir(util.form_path([self.image_path, TEMP_FOLD]))
                        except FileExistsError:
                            pass

                        # Create Cache File
                        input_image = util.form_path([util.dirname(util.absolute(image)), TEMP_FOLD, EQ_IMAGE.format(util.basename(image))])

                        # Equalize Image Histogram
                        image_file = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
                        clahe = cv2.createCLAHE(clipLimit = 1.125, tileGridSize = (4,4))
                        eq_image = clahe.apply(image_file)
                        cv2.imwrite(input_image, eq_image)

                    # Ignore Future Warnings
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore")

                        # Compute Laplace Matrix
                        loaded_image = rgb2gray(io.imread(input_image))
                        laplace_data = laplace(loaded_image, ksize = 10)

                    # Store Image Data
                    image_data[image].vari = variance(laplace_data)
                    image_data[image].nmax = np.amax(laplace_data)
                    image_data[image].rmsv = image_rms
                    image_data[image].lmod = curr_lmod

                # Group Blurry Images
                if ((image_data[image].vari < self.var_threshold) and (image_data[image].nmax < self.max_threshold)):
                    self.blurred.append(image)

                # Update Prompt
                print("\rProcessing Images - {}% ".format(int(curr * 100 / len(self.image_list))), end="")
                curr += 1

            # End Variance Computation---------------------------------------------------------------------------------------------------------------------------------

            # Write Computed Data To Data File
            with open(util.form_path([self.image_path, DATA_FILE]), 'w') as data_file:
                for image in image_data:
                    if (image in self.image_list):
                        data_file.write("{},{},{},{},{}\n".format(image, image_data[image].vari, image_data[image].nmax,
                                                                         image_data[image].rmsv, image_data[image].lmod))
            # Close File
            data_file.close()

            # End Write Operation--------------------------------------------------------------------------------------------------------------------------------------

            # Initialize Diff List
            self.hash_diffs = []

            # Calculate Hash Differences
            for i in range(len(self.hashes) - 1):
                self.hash_diffs.append((self.hashes[i + 1] - self.hashes[i]) * self.precision)

            # End Hash Difference Computation--------------------------------------------------------------------------------------------------------------------------

            # Update Prompt
            print("\rProcessed All Images   ")
        else:
            util.perror("spectra: Found no images to process")

# End Analyze Class----------------------------------------------------------------------------------------------------------------------------------------------------
