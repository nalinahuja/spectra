#Developed by Nalin Ahuja, nalinahuja22

import sys
import util
import shutil

from const import *

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

# Flag Constants
BLUR_SENSITIVITY = "-b"
SCENE_SENSITIVITY = "-s"
DUPLI_SENSITIVITY = "-d"

# Flag List
SPECTRA_FLAGS = [BLUR_SENSITIVITY, SCENE_SENSITIVITY, DUPLI_SENSITIVITY]

# End Defined Constants------------------------------------------------------------------------------------------------------------------------------------------------

def analyze(args):
    # Load Image Module
    import image

    # Analyze Directory
    results = image.analyze(args)

    # Print Scenes Detected
    print("\n*" + str(len(results.scenes)) + " scenes detected*")

    # Print Hash Values
    if (not(util.empty(results.hash_diffs))):
        print("\n*Image Differences*")
        for curr, hash in enumerate(results.hash_diffs, 1):
            print("Difference between images {} and {}: {:02}%".format(curr, curr + 1, hash))

    # Print Blur Array
    if (not(util.empty(results.blurred))):
        print("\n*Possible Blurry Images*")
        for image in results.blurred:
            print(image)

    # Print Duplicates Array
    if (not(util.empty(results.duplicates))):
        print("\n*Possible Duplicate Images*")
        for scene in results.duplicates:
            print(scene)

#End Analyze Function--------------------------------------------------------------------------------------------------------------------------------------------------

def parse(args):
    # Verify Argument List Length
    if (util.empty(args)):
        util.perror("spectra: No arguments found")
    # Verify Directory Existence
    elif (not(util.exists(args[0]))):
        util.perror("spectra: Invalid image path")
    # Verify Argument Count
    elif ((len(args) - 1) % 2):
        util.perror("spectra: Invalid argument format")

    # Initialize Formatted Arguments List
    form_args = []

    # Set Directory Argument
    form_args.append(args[0])

    # Check Arguments For Supported Flags
    for FLAG in SPECTRA_FLAGS:
        # Set Blur Sensitivity Argument
        if (FLAG in args):
            try:
                # Get Threshold Value
                threshold = int(args[args.index(FLAG) + 1])

                # Range Fix Threshold
                if (not(threshold is None)):
                    if (threshold < 0):
                        threshold = 0
                    elif (threshold > 100):
                        threshold = 100
            except ValueError:
                util.perror("spectra: Unexpected argument data type")
            except:
                util.perror("spectra: Fatal error while parsing input arguments")

            # Modify Threshold
            if (FLAG == SCENE_SENSITIVITY):
                threshold = 100 - threshold

            # Add As Formatted Argument
            form_args.append(threshold)
        else:
            # Append Empty Argument
            form_args.append(None)

    # Return Formatted Arguments List
    return (form_args)

# End Util Function----------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Parse Program Arguments
    args = parse(sys.argv[1:])

    try:
        # Analyze Images
        analyze(args)
    except KeyboardInterrupt:
        print("\n\nspectra: Stopped image processing")
    except Exception as e:
        print("\n\nspectra: An unrecoverable error has occurred")
        print(e)

    try:
        # Cleanup Cache Folder
        shutil.rmtree(util.form_path([util.normalize(args[0]), TEMP_FOLD]))
    except OSError:
        pass

# End Main Function----------------------------------------------------------------------------------------------------------------------------------------------------
