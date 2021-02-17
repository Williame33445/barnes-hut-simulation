import tkinter as tk
import csv
import sys
import os

sys.path.append(os.path.abspath("."))

from barneshut.simulationCommand import *

class NumericalForm:
    def __init__(self,rowFactor,master):
        self.options = []
        self.rowFactor = rowFactor
        self.formName = ""
        self.master = master
    
    def get(self, i):
        return float(self.entryText[i].get())
        
    def createForm(self):
        self.entryText = self.emptyStringVarList(len(self.options))
        tk.Label(self.master,text=self.formName).grid(row=1+self.rowFactor,column=0)
        for x in range(len(self.options)):
            tk.Label(self.master,text=self.options[x]).grid(row=2+self.rowFactor,column=2*x)
            tk.Entry(self.master,text=self.entryText[x]).grid(row=2+self.rowFactor, column=2*x+1)

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
    def __init__(self,rowFactor,master):
        NumericalForm.__init__(self,rowFactor,master)
        self.options = ["Half Width","Tick Period","Total Duration","Theta","Max Depth"]
        self.formName = "Simulation Parameters"
        

    def getParams(self):
        return SimulationParams(self.get(0),self.get(1),self.get(2),self.get(3),self.get(4))

    def saveSimulationToFile(self,folder):
        self.saveToFile(folder + "\\simulationParams.csv")

    def loadFromFile(self,folder):
        simulationParamsData = self.getData(folder + "\\simulationParams.csv",1)
        self.setData(simulationParamsData)

class ViewParametersForm(NumericalForm):
    def __init__(self,rowFactor,master):
        NumericalForm.__init__(self,rowFactor,master)
        self.options = ["Width","Zoom","Mass Factor"]
        self.formName = "View Parameters"
        

    def getParams(self):
        return ViewParams(self.get(0),self.get(1),self.get(2))

    def saveSimulationToFile(self,folder):
        self.saveToFile(folder +  "\\viewParams.csv")

    def loadFromFile(self,folder):
        simulationParamsData = self.getData(folder +  "\\viewParams.csv",1)
        self.setData(simulationParamsData)



