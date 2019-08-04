import image

#Analyze Images
grp1 = image.analyze("./images/tests/augmentation")

#Print Scenes Detected
print("*" + str(grp1.detect_scenes()) + " scenes detected*")

#Print Hashing Values
cnt =  1

print("\n*Hash Differences*")
for hash in grp1.hash_diffs:
    print("Difference between images {:02} and {:02}: {}%".format(cnt, cnt + 1, hash))
    cnt += 1

#Print Duplicate Arrays
print("\n*Possible Duplicates*")

for scene in grp1.detect_duplicates():
    print(scene)
