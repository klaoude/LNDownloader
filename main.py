import argparse
import os

from Novel import *

parser = argparse.ArgumentParser()
parser.add_argument("--epub", "-e", help="Output the downloaded chapters as 1 epub.", action="store", dest="epub")
result = parser.parse_args()

if result.epub != None:
    print "[+] The downloaded chapters will be save as epub at {}".format(result.epub)

mkdir(DOWNLOAD_FOLDER)

LN_SITES = LoadJSON("sites.json")

print "Please enter site number."
for i in range(len(LN_SITES)):
    print "({}) {} [{} LNs]".format(i, LN_SITES[i].name, len(LN_SITES[i].LNs))
num = input("Num: ")

print "Please enter LN number."
for i in range(len(LN_SITES[num].LNs)):
    print "({}) {}".format(i, LN_SITES[num].LNs[i].name)
j = input("Num: ")
ln_info = LN_SITES[num].LNs[j].GetChapters()

if result.epub != None:
    print ln_info[0]
    cmd = "txt2epub --keep-line-breaks \"{}\" {}/*.txt --title \"{}\" --language \"FR\"".format(
        ln_info[0].split("/")[-1] + " {}.epub".format(ln_info[1] + "-" + ln_info[2] if ln_info[1] != ln_info[2] else ln_info[1]), 
        ln_info[0].replace(" ", "\ "), 
        ln_info[0].split("/")[-1] + " {}".format(ln_info[1] + "-" + ln_info[2] if ln_info[1] != ln_info[2] else ln_info[1])
    )
    print "[+] Executing: {}".format(cmd)
    #txt2epub --keep-line-breaks Rebirth\ 1-141.epub *.txt --title "Rebirth 1-141" --author "Mad Snail" --language "FR"
    os.system(cmd)    