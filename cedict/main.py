import io

main = {}

file = io.open("cedict_ts.u8", mode="r", encoding = "utf-8")
for string in file.read().split("\n"):
    chineseCharacters = string.split(' ',  1)[1]
    openBracketIndex = chineseCharacters.find('[')
    contentWithinBrackets = chineseCharacters[openBracketIndex +  1:-1]
    remainingPart = chineseCharacters[chineseCharacters.find(']') +  1:]
    resultList = [chineseCharacters[:openBracketIndex].strip(), contentWithinBrackets, remainingPart]
    print(resultList)

