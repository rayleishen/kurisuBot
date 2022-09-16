import random, os
from pathlib import Path


# Random images
imgExtension = ["png", "jpeg", "jpg"] # Image Extensions to be chosen from
allImages = list()

def chooseRandomImage(directory="images"):
    for img in os.listdir(directory): #Lists all files
        ext = img.split(".")[len(img.split(".")) - 1]
        if (ext in imgExtension):
            allImages.append(img)
    choice = random.randint(0, len(allImages) - 1)
    chosenImage = allImages[choice] 
    return chosenImage

def chooseSixDigitNumber():
    return random.randint(1, 440000)

def getCoinFlip():
    coin = random.randint(1, 2)
    if coin == 1:
        return "Heads"
    elif coin == 2:
        return "Tails"

def getDiceRoll():
    return random.randint(1, 6)
