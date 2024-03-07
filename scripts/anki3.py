
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
        if len(temp) == 2:
            dataDict[temp[0]] = [temp[0], temp[1]]
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


if __name__ == "__main__":

    deckNameToCreate = sys.argv[1]
    
    path = "../data/" + sys.argv[2]

    lines = readData(path)
    inputDict = createDictionary(lines)

    try:
        checkAndCreateDeck(deckNameToCreate + " Pinyin")
        
        for term, definition in inputDict.items():
            frontContent = definition[0]
            backContent = definition[1]
            addCardToDeck(deckNameToCreate + " Pinyin", frontContent, backContent)

    except requests.exceptions.RequestException as e:
        print("Error:", e)

