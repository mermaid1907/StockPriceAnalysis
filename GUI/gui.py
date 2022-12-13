import os
from tkinter import *
import ansys_project
import numpy as np

# when you click the button
def button_command():
    # get() method gets the text that you write in the entry box
    var1 = int(entry1.get())
    var2 = int(entry2.get())
    var3 = int(entry3.get())

    #calling module 
    matrix = ansys_project.main(var1, var2, var3)

    # insert() method send the result to Textbox
    output.insert(END, matrix)
    return None
    
def gui(window_title):
    root = Tk()
    # to set the window size
    # root.geometry('400x350')
    root.title(window_title)

    text1 = Label(root, text="First Input", width=17)
    text1.pack()
    global entry1
    entry1 = Entry(root, width=20)
    entry1.pack()

    text2 = Label(root, text="Second Input", width=17)
    text2.pack()
    global entry2
    entry2 = Entry(root, width=20)
    entry2.pack()

    text3 = Label(root, text="Third Input", width=17)
    text3.pack()
    global entry3
    entry3 = Entry(root, width=20)
    entry3.pack()

    spacer1 = Label(root, text="")
    spacer1.pack()
    # we are calling button_command function in Button
    Button(root, text="Calculate", width=17, command=button_command).pack()
    spacer2 = Label(root, text="")
    spacer2.pack()

    # scrol bar and output box
    scroll = Scrollbar(root)
    global output
    output = Text(root, height=8, width=50)
    scroll.pack(side=RIGHT, fill=Y)
    output.pack(side=LEFT, fill=Y)
    scroll.config(command=output.yview)
    output.config(yscrollcommand=scroll.set)

    # to see the window on the screen
    root.mainloop()


if __name__ == "__main__":
    gui("TEI Project")
