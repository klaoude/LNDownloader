#!/usr/bin/python3
import os
import pyperclip
import subprocess
import re

FOLDER = "Downloads/test/"
TRANSLATE = "Translate/"

for file in os.listdir(FOLDER):
    filePath = os.path.join(FOLDER, file)
    with open(filePath, "r", encoding="utf-8") as f:
        continu = True
        while continu:
            content = f.read()
            pyperclip.copy(content)
            subprocess.call(["d:\\Programmes\\Ahk\\AutoHotkey.exe", "translate.ahk"])
            translated = pyperclip.paste()
            if abs(len(content) - len(translated)) > len(content) / 2:
                continu = True
                print("Error translating {} (|content - translated| = {})".format(file, abs(len(content) - len(translated))))
            else:
                continu = False

    
    with open(TRANSLATE + file, "w", encoding="utf-8") as f:
        translated = translated.replace("\xa0", "\r\n")
        translated = re.sub(r"(\r\n)+", "\r\n", translated)
        translated = translated.replace("\r\r", "\r")
        f.write(translated)
        print("File: {} translated !".format(filePath))