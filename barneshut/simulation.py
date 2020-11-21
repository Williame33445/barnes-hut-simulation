import sys
import os
sys.path.append(os.path.abspath("."))

from barneshut.tree import *
from barneshut.calculations import *

def buildTree(initialConditions,halfWidth):
    rootNode = Node(Vector(0.0,0.0),halfWidth)
    addParticles(initialConditions,rootNode)
    rootNode.findMassDistribution()
    return rootNode

def addParticles(initialConditions,rootNode):
    for x in range(len(initialConditions)):
        rootNode.addParticle(initialConditions[x])

def calculateParticlesAcceleration(rootNode,particle):
    return rootNode.calculateNetAcceleration(particle)

def applyAcceleration(initialConditions,rootNode,timeElapsed):
    for x in range(len(initialConditions)):
        acceleration = calculateParticlesAcceleration(rootNode,initialConditions[x])
        changeInVelocity = acceleration.scaled(timeElapsed)
        initialConditions[x].velocity.translate(changeInVelocity)

def applyVelocity(initialConditions,timeElapsed):
    for x in range(len(initialConditions)):
        changeInPosition = initialConditions[x].velocity.scaled(timeElapsed)
        initialConditions[x].pos.translate(changeInPosition)

halfWidth = 50
timeElapsed = 2
duration = 10
numberOfCycles = int(duration/timeElapsed)

initialConditions = [KinematicParticle(1.0,Vector(1.0,-3.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(1.0,-2.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(4.0,-2.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(4.0,-3.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(7.0,-2.0),Vector(1.0,1.0)),KinematicParticle(1.0,Vector(1.0,2.0),Vector(1.0,1.0))]

for z in range(numberOfCycles):
    rootNode = buildTree(initialConditions,halfWidth)
    applyVelocity(initialConditions,timeElapsed)
    applyAcceleration(initialConditions,rootNode,timeElapsed)
#be careful about how close the particles come together absorb function