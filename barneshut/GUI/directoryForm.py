import tkinter as tk
import csv
import sys
import os
from tkinter.constants import LEFT

sys.path.append(os.path.abspath("."))

from barneshut.view import *
from tkinter.filedialog import askdirectory

from barneshut.simulator import *
#generate this at some point
defultDir = "C:/workspace/git-repos/barnes-hut-simulation/barneshut/data/data1"

#this frame allows the user to change the directory
#Its passed into other classes as a parameter and when the user wants to know the directory it uses this class
class DirectoryForm(tk.LabelFrame):
    def __init__(self,parent,BG):
        super().__init__(parent,bg =BG,text="")
        self.folderLocation = defultDir
        self.BG =  BG
        self.directoryText = tk.StringVar()
        self.directoryText.set(self.folderLocation)
        self.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)
        self.layout()

    def layout(self):
        tk.Label(self,text="Current Folder",bg=self.BG).pack(side=tk.LEFT)
        self.directoryEntry = tk.Entry(self,width=100,text=self.directoryText)
        self.directoryEntry.pack(side=tk.LEFT) 
        def directoryChanged(evt):
            self.directoryChanged()
        self.directoryEntry.bind("<FocusOut>",directoryChanged)
        tk.Button(self,text="Change Folder",command=self.chooseFolder).pack(side=tk.LEFT)

    def chooseFolder(self):
        self.folderLocation = askdirectory()
        self.directoryText.set(self.folderLocation)

    def directoryChanged(self):
        self.folderLocation = self.directoryEntry.get()


        