from Novel import *

mkdir(DOWNLOAD_FOLDER)

LoadJSON("sites.json")

print "Please enter site number."
for i in range(len(LN_SITES)):
    print "({}) {} [{} LNs]".format(i, LN_SITES[i].name, len(LN_SITES[i].LNs))
num = input("Num: ")

print "Please enter LN number."
for i in range(len(LN_SITES[num].LNs)):
    print "({}) {}".format(i, LN_SITES[num].LNs[i].name)
j = input("Num: ")
LN_SITES[num].LNs[j].GetChapters()