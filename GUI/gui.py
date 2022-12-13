import os
import numpy as np
import pandas as pd
from tkinter import *

#reading stock codes from scrapped file
def get_stock_codes():
    codes = list()
    data = pd.read_csv('C:\\Users\\Elif Karagoz\\Desktop\\pred\\stock_code_scrap\\stock_code_list.csv', index_col=0)
    for code in data['Code']:
        codes.append(code)
        
    return codes

# when you click the button
def button_command():
    #entry1 and choice are global variables (declared under gui function)
    # get() method gets the text that you write in the entry box
    var1 = entry1.get()
    get_choice = choice.get()
    get_days = days.get()

    #calling module 
    matrix = ansys_project.main(var1)

    # insert() method send the result to Textbox
    output.insert(END, matrix)
    return None
    
def gui(window_title):
    root = Tk()
    # to set the window size
    # root.geometry('400x350')
    root.title(window_title)
    
    
    #to add dropdown items
    global choice
    OPTIONS = get_stock_codes()
    variable = StringVar(root)
    variable.set(OPTIONS[0]) # 0 is the default value
    choice = OptionMenu(root, variable, *OPTIONS)
    choice.pack()

    text1 = Label(root, text="Stock Code:", width=17)
    text1.pack()
    global entry1
    entry1 = Entry(root, width=20)
    entry1.pack()
    
    text2 = Label(root, text="Based on How Many Days:", width=17)
    text2.pack()
    global days
    days = Entry(root, width=20)
    days.pack()

    spacer1 = Label(root, text="")
    spacer1.pack()
    
    # we are calling button_command function in Button
    Button(root, text="Predict", width=17, command=button_command).pack()
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
    gui("Stock Price Pred.")
    
