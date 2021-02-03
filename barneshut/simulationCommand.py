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

#Abstract class whoses subclasses are the methods that the program can be run by
class AbstractSimulationCommand(ABC):
    def __init__(self,particles,simulationParams,viewParams):
        self.particles = particles
        self.simulationParams = simulationParams
        self.viewParams = viewParams
        self.viewCreator = ViewCreator(particles,viewParams)
        self.simulator = Simulator(particles,simulationParams.halfWidth,simulationParams.theta,simulationParams.maxDepth)

    @abstractmethod
    def setUp(self):
        pass

    def simulate(self):
        for t in range(self.simulationParams.numberOfCycles()):
            #applies the accelerations and the velocities to the particles
            self.simulator.tick(self.simulationParams.tickPeriod)
            #updates the video file to take into account the current frame
            self.onTick()

    @abstractmethod
    def onTick(self):
        pass

    @abstractmethod
    def end(self):
        pass

    def execute(self):
        self.setUp()
        self.simulate()
        self.end()

class SimulateToFile(AbstractSimulationCommand):
    def __init__(self,particles,simulationParams,viewParams,fileName,FPS):
        AbstractSimulationCommand.__init__(self,particles,simulationParams,viewParams)
        self.fileName = fileName
        self.FPS = FPS
    def setUp(self):
        fourcc = VideoWriter_fourcc(*'mp4v')
        self.video = VideoWriter(self.fileName, fourcc, self.FPS, (500, 500))
    def onTick(self):
        frame = self.viewCreator.getCurrentView()
        self.video.write(frame)
    def end(self):
        self.video.release()

class SimulateAndShow(AbstractSimulationCommand):
    def __init__(self,particles,simulationParams,viewParams,windowName):
        AbstractSimulationCommand.__init__(self,particles,simulationParams,viewParams)
        self.windowName = windowName


    def setUp(self):
        self.viewCreator = ViewCreator(self.particles,self.viewParams)
        cv2.namedWindow(self.windowName)

    def onTick(self):
        frame = self.viewCreator.getCurrentView()
        cv2.imshow(self.windowName, frame)

        k=cv2.waitKey(1)&0xFF
        return k!=27

    def end(self):
        cv2.destroyAllWindows()