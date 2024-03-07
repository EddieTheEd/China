
import io
from dragonmapper.transcriptions import numbered_to_accented
from dragonmapper.hanzi import to_pinyin

from googletrans import Translator # must use alpha version for some reason, i.e. pip install googletrans==3.1.0a0
import sys

translator = Translator()

main = {}

file = io.open("cedict_ts.u8", mode="r", encoding = "utf-8")
for string in file.read().split("\n"):
    chineseCharacters = string.split(' ',   1)[1]
    openBracketIndex = chineseCharacters.find('[')
    contentWithinBracketsStart = openBracketIndex +  1
    contentWithinBracketsEnd = chineseCharacters.find(']')
    contentWithinBrackets = chineseCharacters[contentWithinBracketsStart:contentWithinBracketsEnd]
    remainingPartStart = chineseCharacters.find(']') +  1
    remainingPart = chineseCharacters[remainingPartStart:].strip()
    resultList = [chineseCharacters[:openBracketIndex].strip(), contentWithinBrackets, remainingPart]
    main[resultList[0]] = resultList


file = open("dict.txt", "w")
for term in main.keys():
    file.write(" ".join(main[term]) + "\n")
file.close()

def translate(filePath):
    uniqueLines = []
    seenLines = set()  # Set to track seen lines
    fileName, fileExtension = filePath.rsplit('.',   1)

    with open(filePath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    # Check if the line has already been processed
                    if line not in seenLines:
                        uniqueLines.append(main[line][0])
                        uniqueLines.append(numbered_to_accented(main[line][1]))
                        uniqueLines.append("<strong>" + main[line][2] + "</strong>")
                        seenLines.add(line)  # Mark the line as seen
                except KeyError:
                    uniqueLines.append(line)
                    uniqueLines.append(to_pinyin(line))
                    uniqueLines.append("<strong>" + translator.translate(line).text + " (GT)</strong>")
                    print(f"Translated {line} via GT")

    with open(f"{fileName}trans.{fileExtension}", 'w') as file:
        file.write('\n'.join(uniqueLines))

filePath = "../data/" + sys.argv[1] 
translate(filePath)
