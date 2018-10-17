import tkinter
import fontawesome

master = tkinter.Tk()

size = 800
divisions = 8

w = tkinter.Canvas(master, width=size, height=size)
w.pack()

for i in range(divisions):
    w.create_line(0, (size / divisions) * i, size, (size / divisions) * i)
    w.create_line((size/divisions) * i, 0, (size/divisions)*i, size )

def click(event):
    #absolute position
    #print("Cursor at X: " + str(event.x) + ", Y: " + str(event.y))

    #column
    for i in range(divisions):
        if(event.x > (size/divisions) * i and event.x < (size/divisions) * (i + 1)):
            #print("Column: " + str(i))
            column = i

    #row
    for i in range(divisions):
        if(event.y > (size/divisions) * i and event.y < (size/divisions) * (i+1)):
            #print("Row: " + str(i))
            row = i

    return(column, row)


w.bind("<Button-1>", click)


tkinter.mainloop()