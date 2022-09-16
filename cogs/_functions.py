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