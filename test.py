import tkinter
from PIL import Image, ImageTk

master = tkinter.Tk()

img = Image.open("sprites/pawn.png")
tatras = ImageTk.PhotoImage(img)

canvas = tkinter.Canvas(master=master, width=img.size[0]+20, height=img.size[1]+20)
canvas.pack()
canvas.create_image(img.size[0]/2+10,img.size[1]/2+10,image=tatras)

master.mainloop()