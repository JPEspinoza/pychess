import tkinter
from PIL import Image, ImageTk, ImageOps
from tkinter import filedialog

###variables
master = tkinter.Tk()

size = 700
divisions = 8
partition = size / divisions

pieceList = []
selectedPiece = None #piece that drew last
tileList = [] #list of tiles the last piece drew

tempTile = None #marked tile when nothing clicked

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

turn = "white"
oppositeTurn = "black"

###classes
class Piece:
    def __init__(self, column, row, side, piece):
        self.column = column
        self.row = row
        self.side = side
        self.tkobject = None #drawing of the piece itself
        self.loadSprite(piece)
        self.type = piece

    def loadSprite(self, piece):
        temp = Image.open("sprites/" + piece + "-" + self.side + ".png")
        offset = partition / 10
        temp.thumbnail((partition-offset,partition- offset))
        self.sprite = ImageTk.PhotoImage(temp)

    def draw(self): #executed every cycle
        #draw itself
        canvas.delete(self.tkobject)
        x = partition * self.column + partition / 2
        y = partition * self.row + partition/ 2
        self.tkobject = canvas.create_image(x, y, image=self.sprite)

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
        index = None
        for i in range(len(pieceList)):
            if pieceList[i].tkobject == self.tkobject:
                index = i
        pieceList.pop(index)
    
    #creates straight line in direction [column, row]
    def lineMark(self, directions):
        for dir in directions:
            column = self.column + dir[0]
            row = self.row + dir[1]
            while(True):
                if(Piece.tryMark(self, column, row) == False):
                    break
                else:
                    column += dir[0]
                    row += dir[1]

    #marks a tile if there is nothing or an enemy
    #returns false if it hits something that cannot be continued in a line
    def tryMark(self,column, row):
        if(column > 7 or row > 7 or column < 0 or row < 0):
            return False

        piece = positionToPiece(column, row)
        if(piece == False):
            self.markTile(column, row)
        elif(piece.side == oppositeTurn):
            self.markTile(column, row)
            return False
        else:
            return False

    def markTile(self, column, row, color = colorPallete["mark"]): #mark a tile as possible to move
        x = column * partition
        y = row * partition

        tkobject = canvas.create_rectangle(x, y, x+partition, y+partition, fill=color)
        tile = Tile(column, row, tkobject)

        tileList.append(tile)

class Pawn(Piece):
    def __init__(self, column, row, side):
        #standard start
        Piece.__init__(self, column, row, side, "pawn")

        #which way can this move
        if(side == "black"):
            self.direction = -1
        else: self.direction = 1

        self.hasMoved = False #allow double move on first turn
    
    def click(self):
        if(positionToPiece(self.column, self.row + self.direction) == False):
            Piece.markTile(self, self.column, self.row+self.direction)
            if(self.hasMoved == False and positionToPiece(self.column, self.row + self.direction *2) == False):
                Piece.markTile(self, self.column, self.row + self.direction *2)
        
        #mark attacks
        if(positionToPiece(self.column -1, self.row + self.direction, oppositeTurn)):
            Piece.markTile(self, self.column -1, self.row + self.direction)
        if(positionToPiece(self.column + 1, self.row + self.direction, oppositeTurn)):
            Piece.markTile(self, self.column + 1, self.row + self.direction)

    def move(self, column, row):
        self.hasMoved = True
        Piece.move(self, column, row)

class Rook(Piece): #torre
    directions = ((1,0), (0,1), (-1,0), (0,-1))
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, side, "rook")
    
    def click(self):
        Piece.lineMark(self, Rook.directions)

class Knight(Piece): #caballo
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, side, "knight")
    
    def click(self):
        moves = ((1,2), (2,1))
        for move in moves:
            for i in [-1, 1]: 
                for r in [-1,1]:
                    Piece.tryMark(self, self.column + move[0] * i, self.row + move[1] * r)

class Bishop(Piece): #alfil
    directions = ((1,1), (-1,1), (1,-1), (-1,-1))
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, side, "bishop")    

    def click(self):
        Piece.lineMark(self, Bishop.directions)

class King(Piece):
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, side, "king")
        self.hasMoved = False

    def castling(self):
        for i in range(1,5):
            pass

    def click(self):
        for i in (-1, 0,1):
            for r in (-1,0,1):
                Piece.tryMark(self, self.column + i, self.row + r)

        if(self.hasMoved == False):
            self.castling()
    
    def move(self, column, row):
        self.hasMoved = True
        Piece.move(self, column, row)

class Queen(Piece):
    directions = ((1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1))
    def __init__(self, column, row, side):
        Piece.__init__(self, column, row, side, "queen")
    
    def click(self):
        Piece.lineMark(self, Queen.directions)

class Tile:
    def __init__(self, column, row, tkobject):
        self.column = column
        self.row = row
        self.tkobject = tkobject

###functions
#delete all pieces, turn to white
def resetGame():
    #this ones are redundant but want to make sure nothing gets away when restarting
    global selectedPiece, tempTile
    canvas.delete(tempTile)
    tempTile = None
    selectedPiece = None

    deleteTiles()
    for piece in pieceList:
        canvas.delete(piece.tkobject)
    pieceList.clear()

def newGame():
    #create pieces
    resetGame()

    global turn, oppositeTurn
    turn = "white"
    oppositeTurn = "black"

    pieceOrder = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook) #helper
    for i in range(0,8):
        #add pawns
        pieceList.append(Pawn(i,6, "black"))
        pieceList.append(Pawn(i,1, "white"))
        #add everything else
        pieceList.append(pieceOrder[i](i, 7, "black"))
        pieceList.append(pieceOrder[i](i, 0, "white"))
    drawPieces()

def loadGame(): #save the game function
    file = filedialog.askopenfile(defaultextension=".pychess")

    if file is None:
        return

    lines = file.readlines()

    if(lines[0] != "pychess-standard-file-format-version-1\n"):
        file.close()
        return

    resetGame()

    for line in lines[1:]:
        temp = line.split()
        
        if(temp[0] == "turn"):
            global turn, oppositeTurn
            turn = temp[1]
            oppositeTurn = temp[2]
        else: #create instances from name
            classes = {"pawn": Pawn, "rook": Rook, "knight": Knight, "bishop": Bishop, "queen": Queen,"king": King}
            pieceList.append(classes[temp[0]](int(temp[1]), int(temp[2]), temp[3]))
            drawPieces()

    file.close()

def saveGame(): #load a game function
    file = filedialog.asksaveasfile(mode='w', defaultextension=".pychess")
    if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return

    file.write("pychess-standard-file-format-version-1\n")

    for piece in pieceList:
        file.write(piece.type + " " + str(piece.column) + " " + str(piece.row) + " "+ piece.side +"\n")
    file.write("turn " + turn + " " + oppositeTurn)

    file.close()

def deleteTiles():
    for tile in tileList:
        canvas.delete(tile.tkobject)
    tileList.clear()

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

    tempTile = canvas.create_rectangle(x, y, x+partition, y+partition, fill=colorPallete["temp"])

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
canvas = tkinter.Canvas(master, width=size, height=size, bg=colorPallete["bg"])
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
        canvas.create_rectangle(column * partition, row* partition, (column+1)*partition, (row+1)*partition, fill=colorPallete["tile"])
        canvas.create_rectangle((column+1) * partition, (row+1)* partition, (column+2)*partition, (row+2)*partition, fill=colorPallete["tile"])

newGame()

#start program
tkinter.mainloop()