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
from cv2 import VideoWriter, VideoWriter_fourcc

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

#Abstract class whoses subclasses are the methods that the program can be run by
class SimulationController:
    def __init__(self,particles,simulationParams,viewParams):
        self.particles = particles
        self.simulationParams = simulationParams
        self.viewParams = viewParams
        self.viewCreator = ViewCreator(particles,viewParams)
        self.simulator = Simulator(particles,simulationParams.halfWidth,simulationParams.theta,simulationParams.maxDepth)
        self.listeners = []

    def setUp(self):
        for l in self.listeners:
            l.setUp()

    def simulate(self):
        for t in range(self.simulationParams.numberOfCycles()):
            #applies the accelerations and the velocities to the particles
            self.simulator.tick(self.simulationParams.tickPeriod)
            #updates the video file to take into account the current frame
            carryOn = self.onTick()
            if not carryOn:
                return

    def onTick(self):
        carryOn = True
        for l in self.listeners:
            if not l.onTick(self.viewCreator.getCurrentView()):
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

class SimulateToFile(SimulationListener):
    def __init__(self,fileName,FPS):
        self.fileName = fileName
        self.FPS = FPS
    def setUp(self):
        fourcc = VideoWriter_fourcc(*'mp4v')
        self.video = VideoWriter(self.fileName, fourcc, self.FPS, (500, 500))
    def onTick(self,currentView):
        self.video.write(currentView)
        return True
    def end(self):
        self.video.release()

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