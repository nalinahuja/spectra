import image

#Analyze Images
grp1 = image.analyze("./images/tests/augmentation")

#Print Scenes Detected
print("*" + str(grp1.detect_scenes()) + " scenes detected*")

#Print Duplicate Count
print("\n*Possible Duplicates*")

dup_arr = grp1.detect_duplicates()

for arr in dup_arr:
    print(arr)
    print("")
