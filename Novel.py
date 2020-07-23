import json
import requests
from tqdm import tqdm
from google.cloud import translate_v2 as translate

from Utils import *

DOWNLOAD_FOLDER = "Downloads"

class Operation():
    def __init__(self, op, maxsplit=0, keep=0, re="", string=""):
        self.op = op
        self.maxsplit = maxsplit
        self.keep = keep
        self.re = re
        self.string = string

    def Execute(self, text):
        if self.op == "refindall":
            return re.findall(self.re, text)
        elif self.op == "resplit":
            return re.split(self.re, text, maxsplit=self.maxsplit)[self.keep]
        elif self.op == "split":
            return text.split(self.string)[self.keep]

class Novel():
    def __init__(self, name, baseurl, findChapter=[], regex=[], reverse=False):
        self.name = name
        self.baseurl = baseurl
        self.findChapter = findChapter
        self.regex = regex
        self.reverse = reverse

    def AddFindChapters(self, op):
        self.findChapter.append(op)

    def AddRegex(self, op):
        self.regex.append(op)

    def download_chapter(self, url, name, path):
        num = re.findall(r"(.*?)(\d+)", name)[0]
        name = "%s%03d" % (num[0], int(num[1]))
        r = requests.get(url)
        content = r.text
        for op in self.regex:
            content = op.Execute(content)
        content = removeHttp(content)

        translate_client = translate.Client()
        result = translate_client.translate(content, target_language="fr")
        print result['translatedText']

        with open(path + "/" + name + ".txt", "w") as f:
            f.write(content.encode("utf-8"))

    def GetChapters(self):
        r = requests.get(self.baseurl)
        text = r.text
        chaps = self.findChapter[0].Execute(text)
        if self.reverse:
            chaps.reverse()
        print "{} chapters found !".format(len(chaps))
        path = DOWNLOAD_FOLDER + "/" + self.name
        print "Downloaded chapters will be download in: {}".format(path)
        mkdir(path)
        inp = raw_input("Witch chapters to download (start-stop): ")
        start = int(inp.split("-")[0])
        stop = int(inp.split("-")[1])
        todown = chaps[start - 1:stop]
        for i in tqdm(range(len(todown))):
            self.download_chapter(todown[i][0], todown[i][1], path)
        #os.system("txt2epub {}/*.txt -o {}".format(DOWNLOAD_FOLDER + "/" + manga_name, manga_name))

class NovelSite():
    def __init__(self, name, url, LNs=[]):
        self.name = name
        self.url = url
        self.LNs = LNs

    def AddNovel(self, novel):
        self.LNs.append(novel)

    def Serialize(self):
        return json.dumps(self, default=convert_to_dict, indent=4)