import sys
import os

sys.path.append(os.path.abspath("."))

import cv2
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *

windowName = 'Circle'

width=10.0
simulationParams = SimulationParams(halfWidth=width/2.0,tickPeriod=2.0,totalDuration=10000)
viewParams = ViewParams(width=width,zoom=50.0,massFactor=5.0E-4)

particles = [KinematicParticle(1.0E4,Vector(1.0,-3.0),Vector(5.0E-4,0.0)), KinematicParticle(1.0E4,Vector(1.0,-2.0),Vector(-5.0E-4,0.0))]

viewCreator = ViewCreator(particles,viewParams)
print('Opening window')
cv2.namedWindow(windowName)
print('Window opened')
def printParticles():
    for p in particles:
        print(p)

def onTick(t):
    print('tick:' + str(t))
    printParticles()

    frame = viewCreator.getCurrentView()
    cv2.imshow(windowName, frame)

    k=cv2.waitKey(1)&0xFF
    return k!=27


print('simulating')

simulator = Simulator(particles,simulationParams.halfWidth)

for t in range(simulationParams.numberOfCycles()):
    simulator.tick(simulationParams.tickPeriod)

    continueSimulation = onTick(t)
    if not continueSimulation:
        break


print('destroying all windows')
cv2.destroyAllWindows()
print('done')
