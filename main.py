from enum import Enum
import tkinter

###constants
master = tkinter.Tk()

size = 500
divisions = 8
partition = size / divisions

canvas = tkinter.Canvas(master, width=size, height=size, bg="peach puff")
canvas.pack()

gameList = []
tileList = []
###

###classes
class Type:
    def __init__(self, sprite, movements, attacks = None):
        self.movements = movements
        if (attacks == None):
            self.attacks = movements
        self.sprite = sprite

class Types(Enum):
    #can move one column, attack one column and one row
    pawnSprite = tkinter.PhotoImage(file="sprites/pawn.png")
    pawnMoves = [[0,1]]
    pawnAttacks = [[1,1], [-1,1]]
    pawn = Type(pawnSprite, pawnMoves, pawnAttacks)

class Piece():
    def __init__(self, column, row, type):
        self.column = column
        self.row = row
        self.type = type
        self.tkobject = None
    
    def draw(self):
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
    for gameObject in gameList:
        gameObject.draw()

    #mark clicked tile
    for tile in tileList:
        canvas.delete(tile)
    tileList.append(canvas.create_rectangle(column * partition, row*partition, (column+1)*partition, (row+1)* partition, fill="red2"))
###

#declare pieces like this
gameList.append(Piece(0,7, Types.pawn))

#init
drawBoard()
canvas.bind("<Button-1>", click)
tkinter.mainloop()

#standard: Columns, Rows