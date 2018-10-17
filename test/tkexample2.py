import tkinter
import fontawesome
from PIL import Image

master = tkinter.Tk()

size = 800

w = tkinter.Canvas(master, width=size, height=size)
w.pack()

img = tkinter.PhotoImage(Image.open("download.gif"))
w.create_image((100,100), img)