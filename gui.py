from tkinter import *
with open('./data/help.txt', 'r') as helpfile:
    help_array = helpfile.readlines()
    help_string = ''
for line in help_array:
    help_string = help_string + line
    
def pop_up():
    layer = Toplevel(root)
    layer.geometry("450x700")
    layer.title("help_window")
    Label(layer, text=help_string).place(x=1, y=1)
    
root = Tk()
root.title("stranded_window")
label = Label(root, text="STRANDED", fg="spring green")
label.pack()
help_button = Button(root, text="HELP", bg="black", command=pop_up, height=2, width=10)
help_button.pack(side=TOP)
start_button = Button(root, text="START", bg="black", height=2, width=10)
start_button.pack()