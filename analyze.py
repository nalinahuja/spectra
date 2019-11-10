#Developed by Nalin Ahuja, nalinahuja22

import sys
import image

def analyze(args):
    #Global Assignment
    global image

    #Analyze Directory
    image_grp = image.process(args)

    #Print Scenes Detected
    print("\n*" + str(len(image_grp.image_scenes)) + " scenes detected*")

    #Print Hashing Values
    if (not(len(image_grp.hash_diffs) == 0)):
        cnt =  1
        print("\n*Image Differences*")
        for hash in image_grp.hash_diffs:
            print("Difference between images {} and {}: {:02}%".format(cnt, cnt + 1, hash))
            cnt += 1

    #Print Duplicates Array
    if (not(len(image_grp.image_duplicates) == 0)):
        print("\n*Possible Duplicate Images*")
        for scene in image_grp.image_duplicates:
            print(scene)

    #Print Blur Array
    if (not(len(image_grp.blurred_images) == 0)):
        print("\n*Possible Blurry Images*")
        for image in image_grp.blurred_images:
            print(image)

#End Analyze Function------------------------------------------------------------------------------------------------------------------------------------------------

def format(args):
    while (len(args) < 4):
        args.append(None)
    return args

#End Util Function---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]

    # try:
    if (len(args) == 0):
        print("ERROR: No Arguments Found")
    else:
        analyze(format(args))
    # except FileNotFoundError:
    #     print("ERROR: Image Load Error")

#End Main Function---------------------------------------------------------------------------------------------------------------------------------------------------
