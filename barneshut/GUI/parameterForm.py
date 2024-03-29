import tkinter as tk
import csv
import sys
import os
from tkinter.constants import LEFT

sys.path.append(os.path.abspath("."))

from barneshut.view import *

from barneshut.simulator import *

BG='#EEEEEE'

#General class that creates a form where you can input data for certain options, it creates its label frame inside
#the parameter label frame 
class NumericalForm(tk.LabelFrame):
    def __init__(self,parent,getFolderLocation,formName,options):
        super().__init__(parent,text=formName,bg=BG)
        self.getFolderLocation = getFolderLocation
        #the headings of the data
        self.options = options
        self.entryText = self.emptyStringVarList(len(options))
        self.layout()
    
    def get(self, i):
        #gets a certain value from the entry points
        return float(self.entryText[i].get())
        
    def layout(self):
        #create the labels of the input and the entry points for the input
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
        #puts data into all the entry points
        for x in range(len(self.options)):
            self.entryText[x].set(float(data[x]))

    def emptyStringVarList(self,length):
        lst = []
        for x in range(length):
            lst.append(tk.StringVar())
        return lst
    
    def saveToFile(self,file):
        #saves the data currently stored in the widgets into a file
        file = open(file,"w")
        file.write(self.printHeaders() + "\n")
        for x in range(len(self.options)):
            #.get(x) automatically turns it into a float
            file.write(str(self.get(x)))
            file.write(",")
        file.close()

    #returns a 2d list [line number][column], if line is 0 then return the all the lines
    def getData(self,location,line):
        #retrives the data currently stored in memory
        data = []
        with open(location, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        if line == 0:
            return data
        else:
            return data[line]

#Class that creates simulation label form
class SimulationParametersForm(NumericalForm):
    def __init__(self,parent,getFolderLocation):
        NumericalForm.__init__(self,parent,getFolderLocation,"Simulation",["Half Width","Tick Period","Total Duration","Theta","Max Depth"])

    def getParams(self):
        #gets the parameters 
        return SimulationParams(self.get(0),self.get(1),self.get(2),self.get(3),self.get(4))

    def saveToFile(self):
        #saves the parameters
        super().saveToFile(self.getFolderLocation() + "/simulationParams.csv")

    def loadFromFile(self):
        #loads the parameters 
        simulationParamsData = self.getData(self.getFolderLocation() + "/simulationParams.csv",1)
        self.setData(simulationParamsData)

#Class that creates simulation form
class ViewParametersForm(NumericalForm):
    def __init__(self,parent,getFolderLocation):
        NumericalForm.__init__(self,parent,getFolderLocation,"View",["Width","Zoom","Mass Factor"])

    def getParams(self):
        #gets the parameters
        return ViewParams(self.get(0),self.get(1),self.get(2))

    def saveToFile(self):
        #saves the parameters
        super().saveToFile(self.getFolderLocation() +  "/viewParams.csv")

    def loadFromFile(self):
        #loads the parameters
        simulationParamsData = self.getData(self.getFolderLocation() +  "/viewParams.csv",1)
        self.setData(simulationParamsData)

#Class that defines the parameter frame inside the tk.frame frame
class ParameterForms(tk.LabelFrame):
    def __init__(self,parent,getFolderLocation):
        super().__init__(parent,text="Parameters",bg=BG)
        self.pack()
        #defines the simulation and view forms inside the the parameter forms form
        self.simulationParametersForm = SimulationParametersForm(self,getFolderLocation)
        self.viewParametersForm = ViewParametersForm(self,getFolderLocation)
        #defines the buttons in the parameter forms frame
        self.layout()

    def layout(self):
        #defines another button frame and puts the buttons in it
        buttonFrame = tk.Frame(self,bg=BG)
        buttonFrame.pack(ipady=15)
        tk.Button(buttonFrame,text="Load Parameters",command=self.load).pack(side=tk.LEFT,padx=10)
        tk.Button(buttonFrame,text="Save Parameters",command=self.save).pack(side=tk.LEFT,padx=10)

    def load(self):
        #gets the data
        self.simulationParametersForm.loadFromFile()
        self.viewParametersForm.loadFromFile()

    def save(self):
        #saves the data to file
        self.simulationParametersForm.saveToFile()
        self.viewParametersForm.saveToFile()

    def getSimulationParameters(self):
        return self.simulationParametersForm.getParams()

    def getViewParameters(self):
        return self.viewParametersForm.getParams()

    def changeFolderLoaction(self,newLocation):
        self.folderLocation = newLocation


