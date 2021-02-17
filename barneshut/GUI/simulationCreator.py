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

#error: The initial particles are not stored unless they are stored in main memory, so running several times means that you don't start at the intial state again, but where you left off.


master = tk.Tk()
master.geometry("1000x300")

FPS = 24

#this part will be removed when load particle options are done properly
def getParticles(location):
    particles = getData(location,0)
    particles.pop(0)
    kinematicParticles = []
    for x in particles:
        kinematicParticles.append(KinematicParticle(float(x[0]),Vector(float(x[1]),float(x[2])),Vector(float(x[3]),float(x[4]))))
    return kinematicParticles
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
        tk.Button(master,text='Save Parameters', command=self.saveAll).place(x=10,y=50*self.factor)
        tk.Button(master,text="Load Parameters",command=self.load).place(x=115,y=50*self.factor)
        tk.Button(master,text="Run",command=self.run).place(x=10,y=80+50*self.factor)
        tk.Checkbutton(master,text="Run to file",variable=self.runType).place(x=50,y=80+50*self.factor)
        tk.Button(master,text="Load Particles and Preview",command=self.viewParticles).place(x=10,y=40+50*self.factor)

    def viewParticles(self):
        self.getAllParameters()
        self.getParticles()
        viewCreator = ViewCreator(self.particles,self.viewParams)
        windowName = "Inital State"
        cv2.namedWindow(windowName)
        frame = viewCreator.getCurrentView()
        cv2.imshow(windowName,frame)


    def load(self):
        self.simulationParametersForm.loadFromFile(self.folderLocation)
        self.viewParametersForm.loadFromFile(self.folderLocation)

    def getAllParameters(self):
        #put errors in here eventually 
        self.simulationParams = self.simulationParametersForm.getParams()
        self.viewParams = self.viewParametersForm.getParams()
        

    def getParticles(self):
        self.particles = getParticles(self.folderLocation + "\\particles.csv")   

    def run(self): 
        self.getAllParameters()
        self.getParticles
        if self.runType.get() == 0:
            command = SimulateAndShow(self.particles,self.simulationParams,self.viewParams,'Circle')
            command.execute()
        elif self.runType.get() == 1:
            command = SimulateToFile(self.particles,self.simulationParams,self.viewParams,self.folderLocation+self.fileName,FPS)
            command.execute()

    def saveAll(self):
        self.simulationParametersForm.saveSimulationToFile(self.folderLocation)
        self.viewParametersForm.saveSimulationToFile(self.folderLocation)
        #need to add particles in here at some point



temp1 = SimulationParametersForm(0,master)
temp2 = ViewParametersForm(2,master)
var = Page(temp2,temp1)
var.runForms()



tk.mainloop()
