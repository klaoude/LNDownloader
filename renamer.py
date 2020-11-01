import os
import re

INPUT = "Downloads/Overgeared (EN)/"
OUTPUT = "Downloads/test/"

for file in os.listdir(INPUT):
    filePath = os.path.join(INPUT, file)
    with open(filePath, "r") as f:
        content = f.read()
        size = len(content)
        if size > 15000:
            print "{} is > 15ko".format(file)
            chapterNum = re.findall(r"Chapter (\d+)-(\d+)", content)
            if len(chapterNum) != 1:
                print "error in regex"
                print chapterNum
            else:
                chapterNum = chapterNum[0]
                print "{}-{}".format(chapterNum[0], chapterNum[1])
                with open(OUTPUT + file[:-4] + "-" + chapterNum[1] + ".txt", "w") as nf:
                    nf.write(content)