from gtts import gTTS 
import requests
import base64
import os
import sys

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
    url = "http://127.0.0.1:8765"
    
    # Add a new note (card) to the deck
    payloadAddCard = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckName,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": []  # Add your desired tags here
            }
        }
    }

    responseAddCard = requests.post(url, json=payloadAddCard)
    responseAddCard.raise_for_status()

    print(f"Card added to the deck {deckName}.\nFront: {front}\nBack: {back}")

def addCardToDeck1(deckName, front, back):
    url = "http://127.0.0.1:8765"
    
    # Add a new note (card) to the deck
    payloadAddCard = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckName,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": []  # Add your desired tags here
            }
        }
    }

    responseAddCard = requests.post(url, json=payloadAddCard)
    responseAddCard.raise_for_status()

    print(f"Card added to the deck {deckName}.\nFront: {front}\nBack: {back}")

def addAudioCardToDeck(deckName, front, back):
    frontmod = front.replace("/", "-")
    frontaudiopath = f"../audios/{frontmod}.mp3"
    url = "http://127.0.0.1:8765"

    mytext = front 
    language = 'zh'
    myobj = gTTS(text=mytext, lang=language, slow=True) 
    myobj.save(frontaudiopath) 

    # Read audio file as binary data
    with open(frontaudiopath, 'rb') as audioFile:
        audioData = base64.b64encode(audioFile.read()).decode('utf-8')

    # Add audio file to Anki's media folder
    media_folder_path = "/home/edwardhuynh/.local/share/Anki2/Chinese/collection.media/"
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
                    "Back": f"{back}"
                },
                "options": {
                    "allowDuplicate": True 
                },
                "tags": []  # Add your desired tags here
            }
        }
    }

    responseAddCard = requests.post(url, json=payloadAddCard)
    responseAddCard.raise_for_status()

    print(f"Card added to the deck {deckName}.\nFront Audio: {frontaudiopath}\nBack: {back}")# The text that you want to convert to audio 




if __name__ == "__main__":

    deckNameToCreate = sys.argv[1]
    
    path = "../data/" + sys.argv[2]

    lines = readData(path)
    inputDict = createDictionary(lines)

    # reading
    
    try:
        checkAndCreateDeck(deckNameToCreate + " Reading")
        
        for term, definition in inputDict.items():
            frontContent = definition[0]
            backContent = definition[1] + " " + definition[2]
            addCardToDeck(deckNameToCreate + " Reading", frontContent, backContent)

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    # writing

    try:
        checkAndCreateDeck(deckNameToCreate + " Writing")
        
        for term, definition in inputDict.items():
            frontContent = definition[1]
            backContent = definition[0] + " " + definition[2]
            addCardToDeck1(deckNameToCreate + " Writing", frontContent, backContent)

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    # listening 

    try:
        checkAndCreateDeck(deckNameToCreate + " Listening")
        
        for term, definition in inputDict.items():
            frontContent = term 
            backContent = definition[0] + " " + definition[1] + " " + definition[2]
            addAudioCardToDeck(deckNameToCreate + " Listening", frontContent, backContent)

    except requests.exceptions.RequestException as e:
        print("Error:", e)




