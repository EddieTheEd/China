from gtts import gTTS 
import os
import sys


filePath = "../data/" +input("Text file path:\n")
frontaudiopath = f"../audios/{filePath}.mp3"

mytext = open(filePath, "r").read()
language = 'zh'
myobj = gTTS(text=mytext, lang=language, slow=True) 
myobj.save(frontaudiopath.replace(".txt", "")) 
print("Done!")
