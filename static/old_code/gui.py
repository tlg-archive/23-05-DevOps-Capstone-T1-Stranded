from tkinter import *
import depos

with open('./data/help.txt', 'r') as helpfile:
    help_array = helpfile.readlines()
    help_string = ''
for line in help_array:
    help_string = help_string + line
    
with open ('./data/title.txt') as title:
    titlelines = title.readlines()
    titlestring = ''
for liens in titlelines:
    titlestring = titlestring + liens

def pop_up():
    layer = Toplevel(root)
    layer.geometry("450x700")
    layer.title("help_window")
    Label(layer, text=help_string).place(x=1, y=1)
    
root = Tk()
root.title("stranded_window")
label = Label(root, text=depos.titlestringgg[0], fg="#000")
label.pack()
help_button = Button(root, text="HELP", command=pop_up, height=2, width=10)
help_button.pack(side=TOP)
start_button = Button(root, text="START", height=2, width=10)
start_button.pack()



root.mainloop()
