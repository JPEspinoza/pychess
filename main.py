import tkinter

class Kind:
    def __init__(self):
        pass

class Piece:
    def __init__(self, position, actions):
        self.position = position
        #array of all possible movements
        self.actions = actions

def drawBoard():    
    for i in range(8):
        canvas.create_line(0, partition*i, size, partition*i)
        canvas.create_line(partition*i, 0, partition*i, size)

#main event in the game
def click(event):
    x, y = event.x, event.y

    #print("X: " + str(x) + " - Y: " + str(y))

    column = None
    row = None
    for i in range(8):
        if(x > i*partition and x < i*partition + partition):
            column = i
        if(y > i*partition and y < i*partition + partition):
            row = i
        pass

    print("Column: " + str(column) + " - Row: " + str(row))

    return column, row

size = 800
partition = size / 8

master = tkinter.Tk()
master.bind('<Button-1>', click)

canvas = tkinter.Canvas(master, width=size, height= size)
canvas.pack()

drawBoard()

tkinter.mainloop()