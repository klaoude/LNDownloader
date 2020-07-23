import requests
import re
import os

DOWNLOAD_FOLDER = "Downloads"

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_chapter(url, name, path):
    num = re.findall(r"(.*?)(\d+)", name)[0]
    name = "%s%03d" % (num[0], int(num[1]))
    r = requests.get(url)
    content = r.text
    content = re.split(r"<p(.*?)><strong>", content, maxsplit=1)[2]
    content = content.split("<div class=\"abh_box abh_box_down abh_box_business\">")[0]
    content = content.replace("</p>", "\n").replace("<br>", "\n").replace("<\\br>", "\n")
    content = re.sub(r"<(.*?)>", "", content)
    content = content.replace("&nbsp;", " ").replace("&amp;", "&")
    with open(path + "/" + name + ".txt", "w") as f:
        f.write(content.encode("utf-8"))
        print name + ".txt Downlaoded !"

def get_chapters(url, manga_name):
    r = requests.get(url)
    reg = re.findall(r"href=\"([^ ]*?)\" title=\"(.*?)\"", r.text)
    path = DOWNLOAD_FOLDER + "/" + manga_name
    mkdir(path)
    for c in reg:
        download_chapter(c[0], c[1], path)
    os.system("txt2epub {}/*.txt -o {}".format(DOWNLOAD_FOLDER + "/" + manga_name, manga_name))

mkdir(DOWNLOAD_FOLDER)

LN_url = "https://xiaowaz.fr/series-en-cours/overgeared/"
get_chapters(LN_url, "overgeared")