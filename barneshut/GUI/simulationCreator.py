import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import cv2

sys.path.append(os.path.abspath("."))

from barneshut.simulationCommand import *
from barneshut.view import *
from barneshut.GUI.numericalForm import *
from cv2 import VideoWriter, VideoWriter_fourcc

simulationParamsOptions = ["Half Width","Tick Period","Total Duration","Theta","Max Depth"]
viewParamsOptions = ["Width","Zoom","Mass Factor"]

master = tk.Tk()
master.geometry("1000x300")

FPS = 24

def getSimulationParamsForScreen(form):
    return SimulationParams(form.get(0),form.get(1),form.get(2),form.get(3),form.get(4))

def getViewParamsForScreen(form):
    return ViewParams(form.get(0),form.get(1),form.get(2))

def getParticles(location):
    particles = getData(location,0)
    particles.pop(0)
    kinematicParticles = []
    for x in particles:
        kinematicParticles.append(KinematicParticle(float(x[0]),Vector(float(x[1]),float(x[2])),Vector(float(x[3]),float(x[4]))))
    return kinematicParticles

#returns a 2d list [line number][column], if line is 0 then return the all the lines
def getData(location,line):
    data = []
    with open(location, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    if line == 0:
        return data
    else:
        return data[line]




class Page:
    def __init__(self,viewParametersForm,simulationParametersForm):
        #sim is 1 view is 2
        self.viewParametersForm = viewParametersForm
        self.simulationParametersForm = simulationParametersForm
        self.fileName = "\\data.mp4"
        self.factor = 2
        #0 is run and show, 1 in simulate to file
        self.runType = tk.IntVar()
        self.folderLocation = "C:\\workspace\\git-repos\\barnes-hut-simulation\\barneshut\\data\\data1"

    def runForms(self):
        self.viewParametersForm.createForm()
        self.simulationParametersForm.createForm()
        tk.Button(master,text='Save', command=self.saveAll).place(x=10,y=50*self.factor)
        tk.Button(master,text="Load",command=self.load).place(x=55,y=50*self.factor)
        tk.Button(master,text="Run",command=self.run).place(x=100,y=50*self.factor)
        tk.Checkbutton(master,text="Run to file",variable=self.runType).place(x=240,y=50*self.factor)
        tk.Button(master,text="View intial state",command=self.viewParticles).place(x=145,y=50*self.factor)

    def viewParticles(self):
        self.getSimulationParameters()
        viewCreator = ViewCreator(self.particles,self.viewParams)
        windowName = "Inital State"
        cv2.namedWindow(windowName)
        frame = viewCreator.getCurrentView()
        cv2.imshow(windowName,frame)


    def load(self):
        simulationParamsData = getData(self.folderLocation + "\\simulationParams.csv",1)
        self.simulationParametersForm.setData(simulationParamsData)
        viewParamsData = getData(self.folderLocation + "\\viewParams.csv",1)
        self.viewParametersForm.setData(viewParamsData)

    def getSimulationParameters(self):
        try:
            self.simulationParams = getSimulationParamsForScreen(self.simulationParametersForm)
            self.viewParams = getViewParamsForScreen(self.viewParametersForm)
            self.particles = getParticles(self.folderLocation + "\\particles.csv")
        except:
            messagebox.showerror("Error","Incorrect data given.")    



    def run(self): 
        self.getSimulationParameters()
        if self.runType.get() == 0:
            command = SimulateAndShow(self.particles,self.simulationParams,self.viewParams,'Circle')
            command.execute()
        elif self.runType.get() == 1:
            command = SimulateToFile(self.particles,self.simulationParams,self.viewParams,self.folderLocation+self.fileName,FPS)
            command.execute()

    def saveAll(self):
        self.saveToFile(self.folderLocation + "\\simulationParams.csv",self.simulationParametersForm)
        self.saveToFile(self.folderLocation + "\\viewParams.csv",self.viewParametersForm)
        #need to add particles in here at some point


    def saveToFile(file,form):
        file = open(file,"w")
        file.write(form.printHeaders() + "\n")
        for x in range(len(form.options)):
            try:
                intData = int(form.data[x].get().strip())
                file.write(str(intData))
                file.write(",")
            except:
                messagebox.showerror("Error","Incorrect data.")
                file.close()
                break
        file.close()




temp = [NumericalForm(simulationParamsOptions,0,"Simulation Parameters",master),NumericalForm(viewParamsOptions,2,"View Parameters",master)]
var = Page(temp[1],temp[0])
var.runForms()



tk.mainloop()
