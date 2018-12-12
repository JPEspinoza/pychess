"""
define all the outer variables
"""

from tkinter import Tk

#read settings from the settings file
settings = open("settings.txt", "r")
lines = settings.readlines()

if(lines.pop(0) != "pychess-settings-version-1\n"):
    exit()

for line in lines:
    temp = line.split()

    if(temp[0] == "size"):
        size = int(temp[1])
    elif(temp[0] == "pallete"):
        if(temp[1] == "blue"):
            colorPallete = {
                "bg": "dark turquoise",
                "tile": "steel blue",
                "temp": "purple",
                "mark": "lawn green",
                "attack": "red"
            }
        else:
            colorPallete = {
                "bg": "peach puff",
                "tiles": "coral",
                "temp": "red",
                "mark": "yellow",
                "attack": "red"
            }

partition = size / 8 #size of the partitions

master = Tk() #window?? not very sure how tkinter works but who cares

#virtual board to keep track of attacks
board = [[None for i in range(8)] for r in range(8)]

pieceList = [] #keep track of pieces themselves
selectedPiece = None #piece clicked last
tileList = [] #list of tiles the last piece drew

tempTile = None #marked tile when nothing clicked

finished = False #did somebody lose?

gameCache = [] #keep state of turns in memory

turn = "white"
oppositeTurn = "black"

debug = True #are we on production or not?

size = None
colorPallete = None
