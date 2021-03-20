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
from barneshut.GUI.particleForm import *

FPS = 24
BG='#EEEEEE'


#Page is a subclass of tk.Frame, where tk.Frame is the largest frame in the application that holds all other label frames
class Page(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #defines the padding for the frame
        self.pack(ipadx=15,ipady=15)
        self.directoryForm = DirectoryForm(self,BG)
        #Creates the parameter form inside the Frame we are manipulating 
        self.parameterForms = ParameterForms(self,self.getFolderLocation) #passing in a function
        self.particleForm = ParticleForm(self,BG,self.getFolderLocation)
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
        tk.Button(buttonFrame,text="Preview",command=self.viewParticles).pack(side=tk.LEFT,padx=10)
        tk.Button(buttonFrame,text="Run",command=self.run).pack(side=tk.LEFT,padx=10)
        tk.Checkbutton(buttonFrame,text="Run to file",variable=self.runType).pack(side=tk.LEFT,padx=10)

    def viewParticles(self):
        #gets the particles from data and then gets the initial frame
        particles = self.particleForm.newParticles()
        viewParams = self.parameterForms.getViewParameters()
        viewCreator = ViewCreator(particles,viewParams)
        windowName = "Initial State"
        cv2.namedWindow(windowName)
        frame = viewCreator.getCurrentView()
        cv2.imshow(windowName,frame)

    def run(self):
        #runs the barnes hut simulation, listeners are created depending on how the simulation is being executed
        particles = self.particleForm.newParticles()
        viewParams = self.parameterForms.getViewParameters()
        simulationParams = self.parameterForms.getSimulationParameters()

        controller = SimulationController(particles,simulationParams,viewParams)
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
