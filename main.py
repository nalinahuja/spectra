import image

#Analyze Images
grp1 = image.analyze("DIRECTORY HERE!")

#Print Scenes Detected
print("*" + str(grp1.detect_scenes()) + " scenes detected*")

#Print Hashing Values
if (not(len(grp1.hash_diffs) == 0)):
    cnt =  1
    print("\n*Hash Differences*")
    for hash in grp1.hash_diffs:
        print("Difference between images {} and {}: {:02}%".format(cnt, cnt + 1, hash))
        cnt += 1

#Print Duplicate Array
if (not(len(grp1.detect_duplicates()) == 0)):
    print("\n*Possible Duplicate Images*")
    for scene in grp1.detect_duplicates():
        print(scene)

#Print Blur Array
if (not(len(grp1.detect_blur()) == 0)):
    print("\n*Possible Blurry Images*")
    for image in grp1.detect_blur():
        print(image)
