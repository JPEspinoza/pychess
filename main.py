from enum import Enum
import tkinter
from PIL import Image, ImageTk, ImageOps

###constants
master = tkinter.Tk()

size = 720
divisions = 8
partition = size / divisions

canvas = tkinter.Canvas(master, width=size, height=size, bg="peach puff")
canvas.pack()

pieceList = [] #list of pieces
selectedPiece = None #piece that drew last
tileList = [] #list of tiles the last piece drew
table = [[],[]] #columns, row

###classes
class Piece:
    def __init__(self, column, row, sprite, side):
        self.column = column
        self.row = row
        self.sprite = sprite
        self.side = side
        self.tkobject = None #placeholder for the drawn piece
    
    def draw(self): #executed every cycle
        #draw itself
        canvas.delete(self.tkobject)
        x = partition * self.column + partition / 2
        y = partition * self.row + partition/ 2
        self.tkobject = canvas.create_image(x, y, image=self.sprite)

class Pawn(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("pawn", side), side) #start the piece
    
    def click(self):
        #draw movements
        pass

class Rook(Piece): #torre
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("rook", side), side)
    pass

class Knight(Piece): #caballo
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("knight", side), side)    

class Bishop(Piece): #alfil
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("bishop", side), side)    
    pass

class King(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("king", side), side)  
    pass

class Queen(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, loadSprite("queen", side), side)
    
    def click(self):
        pass
###
###functions
def loadSprite(piece, side):
    temp = Image.open("sprites/" +piece + "-" + side + ".png")
    temp.thumbnail((partition-10,partition- 10))
    sprite = ImageTk.PhotoImage(temp)
    return sprite

def drawBoard():
    #draw the lines
    for i in range(divisions):
        canvas.create_line(0, partition * i, size, partition * i)
        canvas.create_line(partition * i, 0, partition*i, size )

    #color the tiles
    for row in range(0, divisions, 2):
        for column in range(0, divisions, 2):
            canvas.create_rectangle(column * partition, row* partition, (column+1)*partition, (row+1)*partition, fill="coral")
            canvas.create_rectangle((column+1) * partition, (row+1)* partition, (column+2)*partition, (row+2)*partition, fill="coral")

def click(event): #core game logic
    #check the click position
    column, row = -1, -1
    for i in range(divisions): #column
        if(event.x > partition * i and event.x < partition * (i + 1)):
            #print("Column: " + str(i))
            column = i
    for i in range(divisions): #row
        if(event.y > partition * i and event.y < partition * (i+1)):
            #print("row: " + str(i))
            row = i
    #print("Column: " + str(column) + " - row: " + str(row)) #debug

    #check if a piece was clicked already
    #if there was, then compare against possible movements
    global selectedPiece
    if(selectedPiece != None): #if there is a piece selected then check for marked tiles
        for tile in tileList:
            print(tile)
        return

    #if no piece was clicked then check against pieces
    for piece in pieceList:
        if piece.column == column and piece.row == row:
            piece.click()
            selectedPiece = piece
###

###init
#create pieces
pieceOrder = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
for i in range(0,8):
    #add pawns
    pieceList.append(Pawn(i,6, "black"))
    pieceList.append(Pawn(i,1, "white"))

    pieceList.append(pieceOrder[i](i, 7, "black"))
    pieceList.append(pieceOrder[i](i, 0, "white"))

drawBoard()
canvas.bind("<Button-1>", click)

#draw all pieces
for piece in pieceList:
    piece.draw()

#lets get this started!
tkinter.mainloop()

#standard: Columns, Rows