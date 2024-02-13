from gtts import gTTS 
import requests
import base64
import os

def readData(filePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
    return lines

def createDictionary(lines):
    dataDict = {}
    currentTerm = ""
    currentDefinition = ""
    term = True
    temp = []

    for line in lines:
        line = line.strip()
        temp.append(line)
        if len(temp) == 3:
            dataDict[temp[0]] = [temp[0], temp[1], temp[2]]
            temp = []
    return dataDict

def checkAndCreateDeck(deckName):
    url = "http://127.0.0.1:8765"
    
    # Check if the deck already exists
    payloadCheck = {
        "action": "deckNames",
        "version": 6
    }
    responseCheck = requests.post(url, json=payloadCheck)
    responseCheck.raise_for_status()

    existingDecks = responseCheck.json()

    if deckName not in existingDecks:
        # Deck doesn't exist, create it
        payloadCreate = {
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deckName
            }
        }
        responseCreate = requests.post(url, json=payloadCreate)
        responseCreate.raise_for_status()

        print(f"Deck '{deckName}' created successfully.")
    else:
        print(f"Deck '{deckName}' already exists.")

def addCardToDeck(deckName, front, back):
    frontaudiopath = f"../audios/{front}.mp3"
    url = "http://127.0.0.1:8765"

    mytext = front 
    language = 'zh'
    myobj = gTTS(text=mytext, lang=language, slow=True) 
    myobj.save(frontaudiopath) 

    # Read audio file as binary data
    with open(frontaudiopath, 'rb') as audioFile:
        audioData = base64.b64encode(audioFile.read()).decode('utf-8')

    # Add audio file to Anki's media folder
    media_folder_path = "/home/edwardhuynh/.local/share/Anki2/User 1/collection.media/"
    audio_filename = f"front_audio_{hash(audioData)}.mp3"
    audio_filepath = os.path.join(media_folder_path, audio_filename)

    with open(audio_filepath, 'wb') as audioFile:
        audioFile.write(base64.b64decode(audioData))

    # Add a new note (card) to the deck
    payloadAddCard = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckName,
                "modelName": "Basic",
                "fields": {
                    "Front": f"[sound:{audio_filename}]",
                    "Back": f"{front} {back}"
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": ["yourTag"]  # Add your desired tags here
            }
        }
    }

    responseAddCard = requests.post(url, json=payloadAddCard)
    responseAddCard.raise_for_status()

    print(f"Card added to the deck.\nFront Audio: {frontaudiopath}\nBack: {back}")# The text that you want to convert to audio 


deckNameToCreate = input("What do you want the anki file to be called?\n\n")
    
path = "../data/" + input("Which text file do you want to use? (e.g. output.txt)\n\n")
lines = readData(path)
print("Creating an anki with the following list:")
print(lines)
inputDict = createDictionary(lines)

checkAndCreateDeck(deckNameToCreate)
try:
    for term, definition in inputDict.items():
        frontContent = term
        backContent = definition
        addCardToDeck(deckNameToCreate, frontContent, backContent)

except requests.exceptions.RequestException as e:
    print("Error:", e)



  


    #if __name__ == "__main__":

    #deckNameToCreate = input("What do you want the anki file to be called?\n\n")
    
    #path = "../data/" + input("Which text file do you want to use? (e.g. output.txt)\n\n")

    #lines = readData(path)
    #print("Creating an anki with the following list:")
    #print(lines)
    #inputDict = createDictionary(lines)
    
    #try:
    #checkAndCreateDeck(deckNameToCreate)
        
    #for term, definition in inputDict.items():
    #frontContent = term
    #backContent = definition
    #addCardToDeck(deckNameToCreate, frontContent, backContent)

    #except requests.exceptions.RequestException as e:
    # print("Error:", e)
