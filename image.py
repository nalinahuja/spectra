import os
import imagehash

from PIL import Image

_precision = 1.75

class analyze:
    def __init__(self, path):
        self.image_path = path
        self.scene_threshold = 15
        self.duplicate_threshold = 7.5

        self._get_dir_contents(self.image_path)

        self._calculate_image_hashes()
        self._calculate_hash_differences()

    def _get_dir_contents(self, path):
        #Initialize Image List
        self.image_list = []

        #Store Image Paths
        for file in os.listdir(path):
            if file.endswith((".jpg", ".png", ".jpeg")):
                self.image_list.append(os.path.join(path, file))

        #Sort Image Paths by Number
        self.image_list.sort()

    def _calculate_image_hashes(self):
        #Initialize Hash List
        self.image_hashes = []

        #Calculate Hash Values
        for image in self.image_list:
            self.image_hashes.append(imagehash.average_hash(Image.open(image)))

    def _calculate_hash_differences(self):
        #Initialize Diff List
        self.hash_diffs = []

        #Calculate Hash Differences
        for i in range(0, len(self.image_hashes) - 1):
            self.hash_diffs.append((self.image_hashes[i] - self.image_hashes[i + 1]) * _precision)

    def detect_scenes(self, threshold = None):
        #Process Set Arguments
        if (not(threshold is None)):
            self.scene_threshold = threshold

        #Initialize Scene Count
        scenes = 1

        #Determine Scenes
        for diff in self.hash_diffs:
            if (diff >= self.scene_threshold):
                scenes += 1

        #Return Scene Count
        return scenes

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

        #Return Duplicate Array
        return duplicates

    def detect_blur(self, threshold = None):
        #Process Set Arguments
        if (not(threshold is None)):
            self.duplicate_threshold = threshold

        #Initalize Blurred Images Array
        blurred_images = []

        #Return Blurred Images Array
        return blurred_images
