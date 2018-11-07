from enum import Enum
import tkinter
from PIL import Image, ImageTk, ImageOps

###variables
master = tkinter.Tk()

size = 700
divisions = 8
partition = size / divisions

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
    
    def getIndex(self):
        for i in range(len(pieceList)):
            if pieceList[i].tkobject == self.tkobject:
                return i

    def move(self, column, row):
        #kill any other piece on the tile
        piece = positionToPiece(column, row, oppositeTurn)
        if(piece):
            piece.delete()

        #move to tile
        self.column = column
        self.row = row
        self.draw()
        deleteTiles()
    
    def delete(self):
        #remove drawing
        global canvas
        #remove reference
        pieceList.pop(self.getIndex())

    def checkMove(self,column, row):
        piece = positionToPiece(column, row)
        if(piece == False):
            markTile(column, row)
        elif(piece.side == oppositeTurn):
            markTile(column, row)
            return False
        else:
            return False

class Pawn(Piece):
    def __init__(self, column, row, side):
        #standard start
        Piece.__init__(self, column, row, loadSprite("pawn", side), side)

        #which way can this move
        if(side == "black"):
            self.direction = -1
        else: self.direction = 1

        self.hasMoved = False #allow double move on first turn
    
    def click(self):
        if(positionToPiece(self.column, self.row + self.direction) == False):
            markTile(self.column, self.row+self.direction, "lawn green")
            if(self.hasMoved == False and positionToPiece(self.column, self.row + self.direction *2) == False):
                markTile(self.column, self.row + self.direction *2, "lawn green")
        
        #mark attacks
        if(positionToPiece(self.column -1, self.row + self.direction, oppositeTurn)):
            markTile(self.column -1, self.row + self.direction, "lawn green")
        if(positionToPiece(self.column + 1, self.row + self.direction, oppositeTurn)):
            markTile(self.column + 1, self.row + self.direction, "lawn green")

    def move(self, column, row):
        self.hasMoved = True
        Piece.move(self, column, row)

class Rook(Piece): #torre
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("rook", side), side)
    
    def click(self):
        for i in range(self.column + 1, 8):
            if(Piece.checkMove(self, i, self.row) == False):
                break
        
        for i in range(self.row + 1, 8):
            if(Piece.checkMove(self, self.column, i) == False): break

        for i in range(self.column - 1, -1, -1):
            if Piece.checkMove(self, i, self.row) == False: break
            
        for i in range(self.row -1, -1, -1):
            if Piece.checkMove(self, self.column, i) == False: break

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
def newGame():
    #create pieces
    pieceOrder = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook] #helper
    for i in range(0,8):
        #add pawns
        pieceList.append(Pawn(i,6, "black"))
        pieceList.append(Pawn(i,1, "white"))
        #add everything else
        pieceList.append(pieceOrder[i](i, 7, "black"))
        pieceList.append(pieceOrder[i](i, 0, "white"))
    
    pieceList.append(Rook(4,3,"white"))
    drawPieces()

def loadGame(): #save the game function
    print("load game")

def saveGame(): #load a game function
    print("save game")

def markTile(column, row, color = "lawn green"): #mark a tile as possible to attack
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

#given coordinates returns column and row
def clickToPosition(x,y):
    column, row = -1, -1
    for i in range(divisions): #column
        if(x >= partition * i and x <= partition * (i + 1)):
            column = i
    for i in range(divisions): #row
        if(y >= partition * i and y <= partition * (i+1)):
            row = i

    return column, row

#given a position returns a tile or False
def positionToTile(column, row):
    for tile in tileList:
        if(tile.column == column and tile.row == row):
            return tile
    return False

#given a position and side returns the piece or False
def positionToPiece(column, row, side = None):
    for piece in pieceList:
        if(piece.column == column and piece.row == row):
            if(side != None):
                if(piece.side == side): return piece
            else: return piece
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

    tempTile = canvas.create_rectangle(x, y, x+partition, y+partition, fill="deep sky blue")

def click(event): #core game logic
    #get click
    column, row = clickToPosition(event.x, event.y)
    drawTempTile(column, row)

    piece = positionToPiece(column, row, turn) #select piece, only allow side currently playing

    global selectedPiece

    #core logic
    if(piece): #if piece was clicked then mark tiles
        if(selectedPiece != None): #but if a piece was already selected then first clear the tiles that it marked
            deleteTiles()
        
        piece.click()
        selectedPiece = piece
    elif(positionToTile(column, row)): #if tile was clicked move to the tile, if there is a piece on the tile being moved to then kill that piece
        selectedPiece.move(column, row)
        changeTurn()

    else: #if nothing was clicked mark tile
        drawTempTile(column, row)
        deleteTiles()

    #draw pieces to have everything above potentially marked tiles
    drawPieces()

###init
##TK prepare
canvas = tkinter.Canvas(master, width=size, height=size, bg="peach puff")
canvas.pack()

#create menu
menubar = tkinter.Menu(master) #create menu
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="New Game", command=newGame)
filemenu.add_command(label="Open Game", command=loadGame)
filemenu.add_command(label="Save Game", command=saveGame)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)
master.config(menu=menubar) #display menu

#make clicking run the "click" function that handles all the core logic
canvas.bind("<Button-1>", click)

#draw the board
for i in range(divisions): #create the lines
    canvas.create_line(0, partition * i, size, partition * i)
    canvas.create_line(partition * i, 0, partition*i, size)

for row in range(0, divisions, 2): #color the tiles
    for column in range(0, divisions, 2):
        canvas.create_rectangle(column * partition, row* partition, (column+1)*partition, (row+1)*partition, fill="coral")
        canvas.create_rectangle((column+1) * partition, (row+1)* partition, (column+2)*partition, (row+2)*partition, fill="coral")

newGame()

#start program
tkinter.mainloop()