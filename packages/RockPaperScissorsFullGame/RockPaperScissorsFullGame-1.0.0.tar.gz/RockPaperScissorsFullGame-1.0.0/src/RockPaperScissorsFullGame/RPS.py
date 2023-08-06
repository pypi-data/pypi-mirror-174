from enum import Enum
import random


class Item(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

class Outcome(Enum):
    Win = 1
    Lose = 2
    Tie = 3

def getOutcome(playerItem, computerItem):
    if(playerItem.value == computerItem.value):
        return Outcome.Tie
    elif((playerItem == Item.Rock and computerItem == Item.Scissors) or (playerItem.value == computerItem.value + 1)):
        return Outcome.Win
    else:
        return Outcome.Lose

def getComputerItem():
    index = random.randint(1,3)
    return Item(index)

def inputToItem(str):
    if ("rock").startswith(str.lower()):
        return Item.Rock
    elif ("paper").startswith(str.lower()):
        return Item.Paper
    elif ("scissors").startswith(str.lower()):
        return Item.Scissors
    else:
        return None