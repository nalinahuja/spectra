#Developed by Nalin Ahuja, nalinahuja22

import os
import sys
import image

def analyze(args):
    #Global Assignment
    global image

    #Analyze Directory
    image_grp = image.process(args)

    #Print Scenes Detected
    print("*" + str(len(image_grp.image_scenes)) + " scenes detected*")

    #Print Hashing Values
    if (not(len(image_grp.hash_diffs) == 0)):
        cnt =  1
        print("\n*Hash Differences*")
        for hash in image_grp.hash_diffs:
            print("Difference between images {} and {}: {:02}%".format(cnt, cnt + 1, hash))
            cnt += 1

    #Print Duplicates Array
    # duplicates = image_grp.image_duplicates
    #
    # if (not(len(duplicates) == 0)):
    #     print("\n*Possible Duplicate Images*")
    #     for scene in duplicates:
    #         print(scene)

    #Organize Images
    image_grp.organize_images()

    # #Print Blur Array
    # blurred = image_grp.detect_blur()
    #
    # if (not(len(blurred) == 0)):
    #     print("\n*Possible Blurry Images*")
    #     for image in blurred:
    #         print(image)

#End Analyze Function------------------------------------------------------------------------------------------------------------------------------------------------

def format(args):
    while (len(args) < 4):
        args.append(None)
    return args

#End Util Function---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]

    try:
        if (len(args) == 0):
            print("ERROR: Please Indicate a Valid Directory")
        else:
            analyze(format(args))
    except FileNotFoundError:
        print("ERROR: Directory Error")

#End Main Function---------------------------------------------------------------------------------------------------------------------------------------------------
