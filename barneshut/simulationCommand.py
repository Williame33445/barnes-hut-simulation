from abc import abstractmethod, ABC
import sys
import os

sys.path.append(os.path.abspath("."))

import cv2
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *
from cv2 import VideoWriter, VideoWriter_fourcc

class AbstractSimulationCommand(ABC):
    def __init__(self,particles,simulationParams,viewParams):
        self.particles = particles
        self.simulationParams = simulationParams
        self.viewParams = viewParams
        self.viewCreator = ViewCreator(particles,viewParams)
        self.simulator = Simulator(particles,simulationParams.halfWidth)

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
        frame = viewCreator.getCurrentView()
        cv2.imshow(self.windowName, frame)

        k=cv2.waitKey(1)&0xFF
        return k!=27

    def end(self):
        cv2.destroyAllWindows()

        

def simFileTest():
    fileName = 'C:\\workspace\\bh001.mp4'
    width=10.0
    FPS = 24
    #sets up the initial simulation contiditions, eg how long it will run ect
    simulationParams = SimulationParams(halfWidth=width/2.0,tickPeriod=40.0,totalDuration=100000)
    #sets up the UI
    viewParams = ViewParams(width=width,zoom=50.0,massFactor=5.0E-4)
    particles = [KinematicParticle(1.0E4,Vector(1.0,-3.0),Vector(5.0E-4,0.0)),KinematicParticle(1.0E4,Vector(2.0,-1.0),Vector(5.0E-4,0.0)), KinematicParticle(1.0E4,Vector(1.0,-2.0),Vector(-5.0E-4,0.0))]
    command = SimulateToFile(particles,simulationParams,viewParams,fileName,FPS)
    command.execute()
def simShowTest():
    width=10.0
    #sets up the initial simulation contiditions, eg how long it will run ect
    simulationParams = SimulationParams(halfWidth=width/2.0,tickPeriod=40.0,totalDuration=100000)
    #sets up the UI
    viewParams = ViewParams(width=width,zoom=50.0,massFactor=5.0E-4)
    particles = [KinematicParticle(1.0E4,Vector(1.0,-3.0),Vector(5.0E-4,0.0)),KinematicParticle(1.0E4,Vector(2.0,-1.0),Vector(5.0E-4,0.0)), KinematicParticle(1.0E4,Vector(1.0,-2.0),Vector(-5.0E-4,0.0))]
    command = SimulateAndShow(particles,simulationParams,viewParams,'Circle')
    command.execute()
simFileTest()