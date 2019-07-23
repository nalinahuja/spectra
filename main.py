import image

grp1 = image.analyze("./images/tests/augmentation")

print("*" + str(grp1.detect_scenes()) + " scenes detected*")
print("\n*Possible Duplicates*")

dup_arr = grp1.detect_duplicates()

for arr in dup_arr:
    print(arr)
    print("")
