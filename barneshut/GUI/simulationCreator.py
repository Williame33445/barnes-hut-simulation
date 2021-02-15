import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

sys.path.append(os.path.abspath("."))

from barneshut.getSimulation import *

simulationParamsOptions = ["Half Width","Tick Period","Total Duration","Theta","Max Depth"]
viewParamsOptions = ["Width","Zoom","Mass Factor"]

master = tk.Tk()
master.geometry("1000x300")

class Page:
    def __init__(self,forms,fileName):
        #both of them are lists 
        self.forms = forms
        self.fileName = fileName
        self.factor = len(fileName)


    def runForms(self):
        for x in range(len(self.fileName)):
            self.forms[x].createForm()
        tk.Button(master,text='Save', command=self.saveAll).place(x=10,y=50*self.factor)
        tk.Button(master,text="Load",command=self.load).place(x=55,y=50*self.factor)

    def load(self):
        folderSelected = filedialog.askdirectory()
        barnesHutCLI(folderSelected,runType,fileName)


    def saveAll(self):
        for x in range(len(self.fileName)):
            self.saveToFile(x)


    def saveToFile(self,t):
        file = open(self.fileName[t],"w")
        file.write(self.forms[t].printHeaders() + "\n")
        for x in range(len(self.forms[t].options)):
            try:
                intData = int(self.forms[t].data[x].get().strip())
                file.write(str(intData))
                file.write(",")
            except:
                messagebox.showerror("Error","Incorrect data.")
                file.close()
                break
        file.close()


class Form:
    def __init__(self,options,rowFactor,formName):
        self.options = options
        self.rowFactor = rowFactor
        self.data = []
        self.formName = formName
    
        
    def createForm(self):
        tk.Label(master,text=self.formName).grid(row=1+self.rowFactor,column=0)
        for x in range(len(self.options)):
            tk.Label(master,text=self.options[x]).grid(row=2+self.rowFactor,column=2*x)
            tk.Entry(master).grid(row=2+self.rowFactor, column=2*x+1)
            self.data.append(tk.Entry(master)) 
            self.data[x].grid(row=2+self.rowFactor, column=2*x+1)

    def printHeaders(self):
        line =  ""
        for x in self.options:
            line = line + x + ","
        return line




temp = [Form(simulationParamsOptions,0,"Simulation Parameters"),Form(viewParamsOptions,2,"View Parameters")]
fileNames = ["simulationParams.csv","viewParams.csv"]
var = Page(temp,fileNames)
var.runForms()



tk.mainloop()
