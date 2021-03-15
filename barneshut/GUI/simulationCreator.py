import sys
import os
import tkinter as tk
import cv2


sys.path.append(os.path.abspath("."))

from barneshut.simulationController import *
from barneshut.view import *
from barneshut.GUI.parameterForm import *
from barneshut.GUI.directoryForm import *
from cv2 import VideoWriter, VideoWriter_fourcc

#error: view params or simulation params still seem to get from data1

FPS = 24
BG='#EEEEEE'

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


#Page is a subclass of tk.Frame, where tk.Frame is the largest frame in the application that holds all other label frames
class Page(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #defines the padding for the frame
        self.pack(ipadx=15,ipady=15)
        self.directoryForm = DirectoryForm(self,BG)
        #Creates the parameter form inside the Frame we are manipulating 
        self.parameterForms = ParameterForms(self,self.getFolderLocation) #passing in a function
        self.fileName = "/data.mp4"
        #0 is run and show, 1 in simulate to file
        self.runType = tk.IntVar()
        #Creates the button frame inside the Frame
        self.layout()

    def getFolderLocation(self):
        return self.directoryForm.folderLocation

    def layout(self):
        #intialising the button label frame inside the Frame
        buttonFrame = tk.LabelFrame(self,text="Simulate",bg=BG)
        buttonFrame.pack(ipady=15)
        #defining the buttons inside the button frame
        tk.Button(buttonFrame,text="Run",command=self.run).pack(side=tk.LEFT,padx=10)
        tk.Checkbutton(buttonFrame,text="Run to file",variable=self.runType).pack(side=tk.LEFT,padx=10)
        tk.Button(buttonFrame,text="Load Particles and Preview",command=self.viewParticles).pack(side=tk.LEFT,padx=10)

    def viewParticles(self):
        #gets the particles from data and then gets the initial frame
        self.particles = getParticles(self.getFolderLocation() + "/particles.csv")
        viewParams = self.parameterForms.getViewParameters()
        viewCreator = ViewCreator(self.particles,viewParams)
        windowName = "Initial State"
        cv2.namedWindow(windowName)
        frame = viewCreator.getCurrentView()
        cv2.imshow(windowName,frame)

    def run(self):
        #runs the barnes hut simulation, listeners are created depending on how the simulation is being executed
        if self.particles == None:
            return
        viewParams = self.parameterForms.getViewParameters()
        simulationParams = self.parameterForms.getSimulationParameters()

        controller = SimulationController(self.particles,simulationParams,viewParams)
        #Adds the listeners needed for what the user has selected
        #If the data is being saved to file both listeners will be used
        controller.addListener(SimulateAndShow('Barnes Hut Simulation'))
        if self.runType.get() == 1:
            controller.addListener(SimulateToFile(self.getFolderLocation()+self.fileName,FPS))
        controller.execute()


root = tk.Tk()
root.title('Barnes Hut')
page = Page(root)


tk.mainloop()
