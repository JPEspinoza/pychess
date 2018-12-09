from tkinter import Tk

###variables
master = Tk()

size = 800
divisions = 8
partition = size / divisions

pieceList = []
selectedPiece = None #piece that drew last
tileList = [] #list of tiles the last piece drew

tempTile = None #marked tile when nothing clicked

game = True #did somebody lose?

gameCache = [] #keep state of turns in memory

turn = "white"
oppositeTurn = "black"

debug = True

"""
colorPallete = {
    "bg": "peach puff",
    "tiles": "coral",
    "temp": "red",
    "mark": "yellow",
    "attack": "red"
}
"""
colorPallete = {
    "bg": "dark turquoise",
    "tile": "steel blue",
    "temp": "purple",
    "mark": "lawn green",
    "attack": "?"
}