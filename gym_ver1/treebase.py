from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Olympia Gym - View Member Details')
root.geometry("1000x500")

# Add Some Style
style = ttk.Style()
#Theme
style.theme_use('default')

style.configure("Treeview",
                background= "#D3D3D3",
                foreground = "black",
                rowheight= 25,
                fieldbackground= "#D3D3D3")
