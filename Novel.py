import requests
from requests.api import head
from tqdm import tqdm, trange

from Utils import *

DOWNLOAD_FOLDER = "Downloads"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'Host': 'www.scan-manga.com',
    'Accept': '*/*'
}

s = requests.session()

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
        elif self.op == "follow_redirect":
            ret = []
            filename = "."+self.string.split("/")[-2]+".chap"
            try:
                f = open(filename, "r")
                i = 0
                for l in f.readlines():
                    ret.append((l, text[i][1]))
                    i+=1
            except IOError:
                for i in trange(len(text)):
                    url = self.string + text[i][0] + "/"
                    r = s.get(url, headers=headers, allow_redirects=False)
                    ret.append((r.headers['location'], text[i][1]))
                    with open(filename, "w") as f:
                        for chap in ret:
                            f.write(chap[0]+"\n")
                
            return ret

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
        num = re.findall(r"Ch\.(\d+)(.*)", name)[0]
        name = "Ch.%03d%s" % (int(num[0]), num[1])
        r = s.get(url, headers=headers)
        content = r.text
        for op in self.regex:
            content = op.Execute(content)
        content = removeHttp(content)

        reg = re.findall(r"&(.*?);", content)
        if len(reg) > 0:
            print "[-] Unknown HTML Char: " + str(reg)
            print content
            exit()
        with open(path + "/" + name + ".txt", "w") as f:
            f.write(content.encode("utf-8"))

    def GetChapters(self):
        r = s.get(self.baseurl, headers=headers)
        text = r.text
        for op in self.findChapter:
            text = op.Execute(text)
        chaps = text
        if self.reverse:
            chaps.reverse()
        print "{} chapters found !".format(len(chaps))
        path = DOWNLOAD_FOLDER + "/" + self.name
        print "Downloaded chapters will be download in: {}".format(path)
        mkdir(path)
        inp = raw_input("Witch chapters to download (start-stop): ")
        inpsplit = inp.split("-")
        start = 1
        stop = 1
        if len(inpsplit) == 2:    
            if inpsplit[0].isdigit():
                start = int(inpsplit[0])
            if inpsplit[1].isdigit():
                stop = int(inpsplit[1])
            else:
                stop = len(chaps)
        else:
            start = int(inpsplit[0])
            stop = int(inpsplit[0])
        todown = chaps[start - 1:stop]
        for i in tqdm(range(len(todown))):
            self.download_chapter(todown[i][0], todown[i][1], path)
        return (path, str(start), str(stop))
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