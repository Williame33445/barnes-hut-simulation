import tkinter as tk
import csv
import sys
import os
from tkinter.constants import LEFT

sys.path.append(os.path.abspath("."))

from barneshut.simulationCommand import *

BG='#EEEEEE'

class NumericalForm(tk.LabelFrame):
    def __init__(self,parent,formName,options):
        super().__init__(parent,text=formName,bg=BG)
        self.options = options
        self.entryText = self.emptyStringVarList(len(options))
        self.layout()
    
    def get(self, i):
        return float(self.entryText[i].get())
        
    def layout(self):
        self.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)
        for x in range(len(self.options)):
            tk.Label(self,text=self.options[x],bg=BG).pack(side=tk.LEFT)
            tk.Entry(self,text=self.entryText[x]).pack(side=tk.LEFT)

    def printHeaders(self):
        line =  ""
        for x in self.options:
            line = line + x + ","
        return line

    def setData(self,data):
        for x in range(len(self.options)):
            self.entryText[x].set(float(data[x]))
        # self.createForm()

    def emptyStringVarList(self,length):
        lst = []
        for x in range(length):
            lst.append(tk.StringVar())
        return lst
    
    def saveToFile(self,file):
        file = open(file,"w")
        file.write(self.printHeaders() + "\n")
        for x in range(len(self.options)):
            #.get(x) automatically turns it into a float
            file.write(str(self.get(x)))
            file.write(",")
        file.close()

    #returns a 2d list [line number][column], if line is 0 then return the all the lines
    def getData(self,location,line):
        data = []
        with open(location, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        if line == 0:
            return data
        else:
            return data[line]

class SimulationParametersForm(NumericalForm):
    def __init__(self,parent):
        NumericalForm.__init__(self,parent,"Simulation",["Half Width","Tick Period","Total Duration","Theta","Max Depth"])

    def getParams(self):
        return SimulationParams(self.get(0),self.get(1),self.get(2),self.get(3),self.get(4))

    def saveToFile(self,folder):
        super().saveToFile(folder + "/simulationParams.csv")

    def loadFromFile(self,folder):
        simulationParamsData = self.getData(folder + "/simulationParams.csv",1)
        self.setData(simulationParamsData)

class ViewParametersForm(NumericalForm):
    def __init__(self,parent):
        NumericalForm.__init__(self,parent,"View",["Width","Zoom","Mass Factor"])

    def getParams(self):
        return ViewParams(self.get(0),self.get(1),self.get(2))

    def saveToFile(self,folder):
        super().saveToFile(folder +  "/viewParams.csv")

    def loadFromFile(self,folder):
        simulationParamsData = self.getData(folder +  "/viewParams.csv",1)
        self.setData(simulationParamsData)


class ParameterForms(tk.LabelFrame):
    def __init__(self,parent):
        super().__init__(parent,text="Parameters",bg=BG)
        self.folderLocation = "barneshut/data/data1"
        self.pack()
        self.simulationParametersForm = SimulationParametersForm(self)
        self.viewParametersForm = ViewParametersForm(self)
        self.layout()

    def layout(self):
        buttonFrame = tk.Frame(self,bg=BG)
        buttonFrame.pack(ipady=15)
        tk.Button(buttonFrame,text="Load Parameters",command=self.load).pack(side=tk.LEFT,padx=10)
        tk.Button(buttonFrame,text="Save Parameters",command=self.save).pack(side=tk.LEFT,padx=10)

    def load(self):
        self.simulationParametersForm.loadFromFile(self.folderLocation)
        self.viewParametersForm.loadFromFile(self.folderLocation)

    def save(self):
        self.simulationParametersForm.saveToFile(self.folderLocation)
        self.viewParametersForm.saveToFile(self.folderLocation)

    def getSimulationParameters(self):
        return self.simulationParametersForm.getParams()

    def getViewParameters(self):
        return self.viewParametersForm.getParams()


