import image

grp1 = image.analyze("./images/tests/augmentation_test")

print("*" + str(grp1.detect_scenes()) + " scenes detected*")
print("\n*Possible Duplicates*")
print(grp1.detect_duplicates())
