import sys
import os

sys.path.append(os.path.abspath("."))

import cv2
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *
from cv2 import VideoWriter, VideoWriter_fourcc

fileName = 'bh001.mp4'

width=10.0
height=10.0
FPS = 24
#sets up the initial simulation contiditions, eg how long it will run ect
simulationParams = SimulationParams(halfWidth=width/2.0,tickPeriod=40.0,totalDuration=100000)
#sets up the UI
viewParams = ViewParams(width=width,zoom=50.0,massFactor=5.0E-4)

particles = [KinematicParticle(1.0E4,Vector(1.0,-3.0),Vector(5.0E-4,0.0)),KinematicParticle(1.0E4,Vector(2.0,-1.0),Vector(5.0E-4,0.0)), KinematicParticle(1.0E4,Vector(1.0,-2.0),Vector(-5.0E-4,0.0))]

#creates a mp4 file that can be written to
viewCreator = ViewCreator(particles,viewParams)
fourcc = VideoWriter_fourcc(*'mp4v')
video = VideoWriter(fileName, fourcc, FPS, (500, 500))

def printParticles():
    for p in particles:
        print(p)

def addFrame():
    frame = viewCreator.getCurrentView()
    video.write(frame)

print('simulating')
#At the moment this represents the initial conitions of the system, but as the system is ticked it will find the next set of conditions for the next frame by applying forces.
simulator = Simulator(particles,simulationParams.halfWidth)

#runs for the set amount of time required then stops
for t in range(simulationParams.numberOfCycles()):
    #applies the accelerations and the velocities to the particles
    simulator.tick(simulationParams.tickPeriod)
    #updates the video file to take into account the current frame
    addFrame()

    print('tick')
    printParticles()


video.release()
print('done')
