import os
import sys
import image

try:
    #Analyze Images
    image_grp = image.analyze(os.path.normpath(sys.argv[1]))

    #Print Scenes Detected
    print("*" + str(image_grp.detect_scenes()) + " scenes detected*")

    #Print Hashing Values
    if (not(len(image_grp.hash_diffs) == 0)):
        cnt =  1
        print("\n*Hash Differences*")
        for hash in image_grp.hash_diffs:
            print("Difference between images {} and {}: {:02}%".format(cnt, cnt + 1, hash))
            cnt += 1

    #Print Duplicate Array
    if (not(len(image_grp.detect_duplicates()) == 0)):
        print("\n*Possible Duplicate Images*")
        for scene in image_grp.detect_duplicates():
            print(scene)

    #Print Blur Array
    if (not(len(image_grp.detect_blur()) == 0)):
        print("\n*Possible Blurry Images*")
        for image in image_grp.detect_blur():
            print(image)
except IndexError:
    print("ERROR: Please Indicate a Directory!")
except FileNotFoundError:
    print("ERROR: Invalid Directory!")
