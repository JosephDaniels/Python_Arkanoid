import random

from functools import partial

import tkinter as tk

from tkinter import ttk, messagebox

class Entry_Window(tk.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.master = master
        self.title = message
        self.create_widgets()
    def create_widgets(self):
        print ("Prompt!!")
        pass

class Settings_Window(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master



def test_1():  # testing the whole thing together
    root = tk.Tk()
    root.withdraw()
    myapp = Settings_Window(root)
    myapp.mainloop()

if __name__ == "__main__":
    test_1()