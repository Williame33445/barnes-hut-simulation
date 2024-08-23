from abc import abstractmethod, ABC
import sys
import os
import csv

sys.path.append(os.path.abspath("."))

import cv2
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *
from cv2 import VideoWriter

"""Listeners are required so the user can run the program with both settings at the same time, while not having to 
run it literally twice. The functions of simulation listener are defined as the functions that are called differently
by the 2 ways that functions can be run."""
class SimulationListener(ABC):

    @abstractmethod
    def setUp(self):
        pass

    @abstractmethod
    def onTick(self,currentView):
        pass

    @abstractmethod
    def end(self):
        pass

#Class that defines the comman functions between the 2 ways the simulation can be executed
class SimulationController:
    def __init__(self,particles,simulationParams,viewParams):
        self.particles = particles
        self.simulationParams = simulationParams
        self.viewParams = viewParams
        self.viewCreator = ViewCreator(particles,viewParams)
        self.simulator = Simulator(particles,simulationParams.halfWidth,simulationParams.theta,simulationParams.maxDepth)
        self.listeners = []

    def setUp(self):
        #calls set up on all of the listeners
        for l in self.listeners:
            l.setUp()

    def simulate(self):
        for t in range(self.simulationParams.numberOfCycles()):
            #applies the accelerations and the velocities to the particles
            self.simulator.tick(self.simulationParams.tickPeriod)
            #checks to see if any of the listeners want to stop
            carryOn = self.onTick()
            if not carryOn:
                return

    def onTick(self):
        carryOn = True
        currentView = self.viewCreator.getCurrentView()
        #if any of the listeners onTick is false then the program is stoped
        for l in self.listeners:
            if not l.onTick(currentView):
                carryOn =  False
        return carryOn

    def end(self):
        for l in self.listeners:
            l.end()

    def addListener(self,l):
        self.listeners.append(l)

    def execute(self):
        self.setUp()
        self.simulate()
        self.end()

#Subclass the the listener that deals with simulations to file
class SimulateToFile(SimulationListener):
    def __init__(self,fileName,FPS,pixels):
        self.fileName = fileName
        self.FPS = FPS
        self.pixels = pixels

    def setUp(self):
        fourcc = VideoWriter.fourcc(*'mp4v')
        self.video = VideoWriter(self.fileName, fourcc, self.FPS, (self.pixels, self.pixels)) 

    def onTick(self,currentView):
        self.video.write(currentView)
        return True
    
    def end(self):
        self.video.release()

#Subclass the the listener that deals with simulations directly to the screen
class SimulateAndShow(SimulationListener):
    def __init__(self,windowName):
        self.windowName = windowName

    def setUp(self):
        cv2.namedWindow(self.windowName)

    def onTick(self,currentView):
        cv2.imshow(self.windowName, currentView)

        k=cv2.waitKey(1)&0xFF
        return k!=27

    def end(self):
        cv2.destroyAllWindows()