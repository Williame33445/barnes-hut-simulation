import sys
import os
sys.path.append(os.path.abspath("."))

from barneshut.tree import *

halfWidth = 50
timeElapsed = 2
duration = 100
numberOfCycles = duration/timeElapsed

#need to change this the kinematic particle to define velocities
initialConditions = [particle(1.0,-3.0,-3.0),particle(1.0,-2.0,-3.0),particle(4.0,-2.0,-1.0),particle(4.0,-3.0,-3.5),particle(7.0,-2.0,1.0),particle(1.0,2.0,-3.0)]

def buildTree(initialConditions,rootNode):
    for x in initialConditions:
        rootNode.addParticle(initialConditions[x])

def calculateParticlesAcceleration(initialConditions):
    acceleration = []
    for z in initialConditions:
        acceleration[z] = rootNode.calculateNetAcceleration(z)
    return acceleration

#def applyAcceleration(velocity,acceleration,timeElapsed):
#    changeInVelocity = acceleration.scaled(timeElapsed)

#def changeInPosition(velocity,initialConditions,timeElapsed):
#    changeInDistance = velocity.scaled(timeElapsed)

#should be a for loop around for numberOfCycles
rootNode = Node(Vector(0.0,0.0),halfWidth)
buildTree(initialConditions,rootNode)

rootNode.findMassDistribution()
acceleration = calculateParticlesAcceleration(initialConditions)
#then apply the changes in distance and velociy