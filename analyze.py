import os
import sys
import image

#End Imports-------------------------------------------------------------------------------------------------------------------------------------------

def analyze(dir, scene_threshold = None, duplicate_threshold = None, blur_threshold = None):
    #Global Assignment
    global image

    #Analyze Images
    image_grp = image.analyze(os.path.normpath(dir))

    #Print Scenes Detected
    print("*" + str(image_grp.detect_scenes(threshold = scene_threshold)) + " scenes detected*")

    #Print Hashing Values
    if (not(len(image_grp.hash_diffs) == 0)):
        cnt =  1
        print("\n*Hash Differences*")
        for hash in image_grp.hash_diffs:
            print("Difference between images {} and {}: {:02}%".format(cnt, cnt + 1, hash))
            cnt += 1

    #Print Duplicate Array
    if (not(len(image_grp.detect_duplicates(threshold = duplicate_threshold)) == 0)):
        print("\n*Possible Duplicate Images*")
        for scene in image_grp.detect_duplicates(threshold = duplicate_threshold):
            print(scene)

    #Print Blur Array
    if (not(len(image_grp.detect_blur(threshold = blur_threshold)) == 0)):
        print("\n*Possible Blurry Images*")
        for image in image_grp.detect_blur(threshold = blur_threshold):
            print(image)

#End Analyze Function----------------------------------------------------------------------------------------------------------------------------------

def format(arr):
    for i in range(len(arr)):
        if (arr[i] == str("def")):
            arr[i] = None
        elif (i > 0):
            arr[i] = int(arr[i])

#End Util Function-------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    data_in = []
    no_error = True

    #Param Ingest
    try:
        data_in.append(sys.argv[1])
        data_in.append(sys.argv[2])
        data_in.append(sys.argv[3])
        data_in.append(sys.argv[4])

    #Missing Param Catch
    except IndexError:
        no_error = False

        #Format data_in
        format(data_in)

        #Determine Param Count
        if (len(data_in) == 0):
            print("ERROR: Please Indicate a Directory!")
        elif (len(data_in) == 1):
            analyze(data_in[0])
        elif (len(data_in) == 2):
            analyze(data_in[0], scene_threshold = data_in[1])
        elif (len(data_in) == 3):
            analyze(data_in[0], scene_threshold = data_in[1], duplicate_threshold = data_in[2])

    #Invlaid File Location Catch
    except FileNotFoundError:
        print("ERROR: Invalid Directory!")

    #Complete Param List Analyze Call
    if (no_error):
        #Format data_in
        format(data_in)

        #Call analyze Function
        analyze(data_in[0], scene_threshold = data_in[1], duplicate_threshold = data_in[2], blur_threshold = data_in[3])

#End Main Function-------------------------------------------------------------------------------------------------------------------------------------
