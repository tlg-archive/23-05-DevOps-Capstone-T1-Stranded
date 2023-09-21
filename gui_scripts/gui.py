from tkinter import *

root = Tk()
root.title("stranded_window")

label = Label(root, text="STRANDED", fg="spring green")
label.pack()

button = Button(root, text="START", bg="black", height=2, width=10)
button.pack()

main_entry = Entry(root, width=30)
main_entry.pack()

root.mainloop()