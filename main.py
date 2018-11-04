from enum import Enum
import tkinter
from PIL import Image, ImageTk, ImageOps

###variables
master = tkinter.Tk()

size = 720
divisions = 8
partition = size / divisions

canvas = tkinter.Canvas(master, width=size, height=size, bg="peach puff")
canvas.pack()

pieceList = []
selectedPiece = None #piece that drew last
tileList = [] #list of tiles the last piece drew

tempTile = None #marked tile when nothing clicked

turn = "white"
oppositeTurn = "black"

###classes
class Piece:
    def __init__(self, column, row, sprite, side):
        self.column = column
        self.row = row
        self.sprite = sprite
        self.side = side
        self.tkobject = None #drawing of the piece itself

    def draw(self): #executed every cycle
        #draw itself
        canvas.delete(self.tkobject)
        x = partition * self.column + partition / 2
        y = partition * self.row + partition/ 2
        self.tkobject = canvas.create_image(x, y, image=self.sprite)

    def move(self, column, row):
        self.column = column
        self.row = row
        self.draw()
        deleteTiles()

class Pawn(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("pawn", side), side) #start the piece
        if(side == "black"):
            self.direction = -1
        else: self.direction = 1
    
    def click(self):
        markTile(self.column, self.row+self.direction, "yellow")

class Rook(Piece): #torre
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("rook", side), side)
    
    def click(self):
        pass

class Knight(Piece): #caballo
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("knight", side), side)
    
    def click(self):
        pass

class Bishop(Piece): #alfil
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("bishop", side), side)    

    def click(self):
        pass

class King(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("king", side), side)  

    def click(self):
        pass

class Queen(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("queen", side), side)
    
    def click(self):
        pass

class Tile:
    def __init__(self, column, row, tkobject):
        self.column = column
        self.row = row
        self.tkobject = tkobject

###functions
def markTile(column, row, color): #mark a tile as possible to attack
    x = column * partition
    y = row * partition

    tkobject = canvas.create_rectangle(x, y, x+partition, y+partition, fill=color)
    tile = Tile(column, row, tkobject)

    tileList.append(tile)

def deleteTiles():
    for tile in tileList:
        canvas.delete(tile.tkobject)
    tileList.clear()

def loadSprite(piece, side):
    temp = Image.open("sprites/" +piece + "-" + side + ".png")
    temp.thumbnail((partition-10,partition- 10))
    sprite = ImageTk.PhotoImage(temp)
    return sprite

#draws the entire board
def createBoard():
    for i in range(divisions): #create the lines
        canvas.create_line(0, partition * i, size, partition * i)
        canvas.create_line(partition * i, 0, partition*i, size)

    for row in range(0, divisions, 2): #color the tiles
        for column in range(0, divisions, 2):
            canvas.create_rectangle(column * partition, row* partition, (column+1)*partition, (row+1)*partition, fill="coral")
            canvas.create_rectangle((column+1) * partition, (row+1)* partition, (column+2)*partition, (row+2)*partition, fill="coral")

def createPieces():
    #create pieces
    pieceOrder = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook] #temporal helper
    for i in range(0,8):
        #add pawns
        pieceList.append(Pawn(i,6, "black"))
        pieceList.append(Pawn(i,1, "white"))

        pieceList.append(pieceOrder[i](i, 7, "black"))
        pieceList.append(pieceOrder[i](i, 0, "white"))

#given coordinates returns column and row
def clickToPosition(x,y):
    column, row = -1, -1
    for i in range(divisions): #column
        if(x >= partition * i and x <= partition * (i + 1)):
            column = i
    for i in range(divisions): #row
        if(y >= partition * i and y <= partition * (i+1)):
            row = i

    #print("Column: " + str(column) + " - Row:" + str(row))
    return column, row

#given a position returns the piece in the tile, the marked tile with potentially a piece on it or False
def positionToPiece(column, row):
    for tile in tileList:
        if(tile.column == column and tile.row == row):
            return tile

    for piece in pieceList:
        if(piece.column == column and piece.row == row and piece.side == turn):
            return piece

    return False

def drawPieces():
    for piece in pieceList:
        piece.draw()

def changeTurn():
    global turn, oppositeTurn, selectedPiece
    turn, oppositeTurn = oppositeTurn, turn
    selectedPiece = None
    deleteTiles()

#draw a tile, marking what was clicked
def drawTempTile(column, row):
    global tempTile
    canvas.delete(tempTile)

    x = column * partition
    y = row * partition

    tempTile = canvas.create_rectangle(x, y, x+partition, y+partition, fill="red")

def click(event): #core game logic
    #get click
    column, row = clickToPosition(event.x, event.y)
    drawTempTile(column, row)

    clickObject = positionToPiece(column, row)

    global selectedPiece

    #core logic
    if(isinstance(clickObject, Piece)): #if piece was clicked then mark tiles

        if(selectedPiece != None): #but if a piece was already selected then first clear the tiles that it marked
            deleteTiles()
        
        clickObject.click()
        selectedPiece = clickObject

    elif(isinstance(clickObject, Tile)): #if tile was clicked move to the tile, if there is a piece on the tile being moved to then kill that piece
        selectedPiece.move(column, row)
        changeTurn()

    else: #if nothing was clicked mark tile
        deleteTiles()

    #draw pieces to have everything above potentially marked tiles
    drawPieces()

###init
#make clicking run the "click" function that handles all the core logic
canvas.bind("<Button-1>", click)

createPieces()
createBoard()
drawPieces()

#lets get this started!
tkinter.mainloop()

#standard: Columns, Rows