from enum import Enum
import tkinter
from PIL import Image, ImageTk, ImageOps

###constants
master = tkinter.Tk()

size = 500
divisions = 8
partition = size / divisions

canvas = tkinter.Canvas(master, width=size, height=size, bg="peach puff")
canvas.pack()

pieceList = []
tileList = []
###

###classes
class Piece():
    def __init__(self, column, row, sprite, movements, attacks):
        self.column = column
        self.row = row
        self.sprite = sprite
        self.movements = movements
        self.attacks = attacks
        self.tkobject = None #placeholder for the drawn piece
        self.tiles = [] #placeholder for the drawn
    
    def draw(self): #executed every cycle
        #draw self
        canvas.delete(self.tkobject)
        x = partition * self.column + partition / 2
        y = partition * self.row + partition/ 2
        self.tkobject = canvas.create_image(x, y, image=self.sprite)

        #delete the tiles if the piece wasn't clicked
        for tile in self.tiles:
            canvas.delete(tile)
    
    def click(self): #executed only on click
        pass

class Pawn(Piece):
    def __init__(self, column, row):
        #data of the pawn
        temp = Image.open("sprites/pawn.png")
        temp.thumbnail((partition,partition))

        pawnSprite = ImageTk.PhotoImage(temp)

        pawnMoves = [[0,1]]
        pawnAttacks = [[1,1], [-1,1]]

        Piece.__init__(self, column, row, pawnSprite, pawnMoves, pawnAttacks)

class Rook(Piece): #torre
    pass

class Knight(Piece): #caballo
    pass

class Bishop(Piece): #alfil
    pass

class King(Piece):
    pass

class Queen(Piece):
    pass
###

###create the board
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
###

###core game logic
def click(event):
    ###check the click position
    column, row = -1, -1
    for i in range(divisions): #column
        if(event.x > partition * i and event.x < partition * (i + 1)):
            #print("Column: " + str(i))
            column = i
    for i in range(divisions): #row
        if(event.y > partition * i and event.y < partition * (i+1)):
            #print("row: " + str(i))
            row = i
    print("Column: " + str(column) + " - row: " + str(row))
    ###

    ###draw everything else
    #mark clicked tile
    for tile in tileList:
        canvas.delete(tile)
    
    tileList.append(canvas.create_rectangle(column * partition, row*partition, (column+1)*partition, (row+1)* partition, fill="red2"))

    #draw pieces
    for piece in pieceList:
        piece.draw()

    #check if there is a piece on the tile
    for piece in pieceList:
        if piece.column == column and piece.row == row:
            piece.click()
            pass
###

#declare pieces like this
pieceList.append(Pawn(0,6))

#init
drawBoard()
canvas.bind("<Button-1>", click)
tkinter.mainloop()

#standard: Columns, Rows