def removeDuplicates(filePath):
    uniqueLines = set()
    fileName, fileExtension = filePath.rsplit('.', 1)

    with open(filePath, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                if line not in uniqueLines:
                    uniqueLines.add(line)

    with open(f"{fileName}prep.{fileExtension}", 'w') as file:
        file.write('\n'.join(uniqueLines))

filePath = "../data/" + input("Please input the text file path.\n\n") 
removeDuplicates(filePath)
print("Finished checking duplicates for path " + filePath)
