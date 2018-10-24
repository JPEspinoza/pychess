import tkinter

###constants
master = tkinter.Tk()

size = 500
divisions = 8
partition = size / divisions

canvas = tkinter.Canvas(master, canvasidth=size, height=size, bg="peach puff")
canvas.pack()
###

###create the board
#dracanvas the lines
for i in range(divisions):
    canvas.create_line(0, partition * i, size, partition * i)
    canvas.create_line(partition * i, 0, partition*i, size )

#color the tiles
for rocanvas in range(0, divisions, 2):
    for column in range(0, divisions, 2):
        canvas.create_rectangle(column * partition, rocanvas* partition, (column+1)*partition, (rocanvas+1)*partition, fill="coral")
        canvas.create_rectangle((column+1) * partition, (rocanvas+1)* partition, (column+2)*partition, (rocanvas+2)*partition, fill="coral")
###

###core game logic
color = None
def click(event):
    #absolute position
    column, rocanvas = -1, -1
    #print("Cursor at X: " + str(event.x) + ", Y: " + str(event.y))

    #column
    for i in range(divisions):
        if(event.x > partition * i and event.x < partition * (i + 1)):
            #print("Column: " + str(i))
            column = i

    #rocanvas
    for i in range(divisions):
        if(event.y > partition * i and event.y < partition * (i+1)):
            #print("Rocanvas: " + str(i))
            rocanvas = i

    print("Column: " + str(column) + " - Rocanvas: " + str(rocanvas))

    #change color of the tile clicked
    global color
    canvas.delete(color)
    color = canvas.create_rectangle(column * partition, rocanvas*partition, (column+1)*partition, (rocanvas+1)* partition, fill="red2")
###

#init
canvas.bind("<Button-1>", click)
tkinter.mainloop()