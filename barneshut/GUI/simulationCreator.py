import sys
import os
import tkinter as tk
import cv2

sys.path.append(os.path.abspath("."))

from barneshut.simulationController import *
from barneshut.view import *
from barneshut.GUI.parameterForm import *
from cv2 import VideoWriter, VideoWriter_fourcc

#error: The initial particles are not stored unless they are stored in main memory, so running several times means that you don't start at the intial state again.

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


class Page(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(ipadx=15,ipady=15)
        self.parameterForms = ParameterForms(self)
        self.fileName = "/data.mp4"
        #0 is run and show, 1 in simulate to file
        self.runType = tk.IntVar()
        self.folderLocation = "barneshut/data/data2"
        self.layout()

    def layout(self):
        buttonFrame = tk.LabelFrame(self,text="Simulate",bg=BG)
        buttonFrame.pack(ipady=15)
        tk.Button(buttonFrame,text="Run",command=self.run).pack(side=tk.LEFT,padx=10)
        tk.Checkbutton(buttonFrame,text="Run to file",variable=self.runType).pack(side=tk.LEFT,padx=10)
        tk.Button(buttonFrame,text="Load Particles and Preview",command=self.viewParticles).pack(side=tk.LEFT,padx=10)

    def viewParticles(self):
        self.particles = getParticles(self.folderLocation + "/particles.csv")
        viewParams = self.parameterForms.getViewParameters()
        viewCreator = ViewCreator(self.particles,viewParams)
        windowName = "Initial State"
        cv2.namedWindow(windowName)
        frame = viewCreator.getCurrentView()
        cv2.imshow(windowName,frame)

    def run(self):
        if self.particles == None:
            return
        viewParams = self.parameterForms.getViewParameters()
        simulationParams = self.parameterForms.getSimulationParameters()
        controller = SimulationController(self.particles,simulationParams,viewParams)
        controller.addListener(SimulateAndShow('Barnes Hut Simulation'))
        if self.runType.get() == 1:
            controller.addListener(SimulateToFile(self.folderLocation+self.fileName,FPS))
        controller.execute()


root = tk.Tk()
root.title('Barnes Hut')
Page(root)

tk.mainloop()
