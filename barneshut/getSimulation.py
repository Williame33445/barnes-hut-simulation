import sys
import os

sys.path.append(os.path.abspath("."))

from barneshut.simulationCommand import *
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *

dataLocation = "C:\\workspace\\git-repos\\barnes-hut-simulation\\barneshut\\data"
fileName = 'C:\\workspace\\bh001.mp4'
width = 10.0
FPS = 24

def getData(location):
    data = []
    with open(location, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def getSimulationParams(location,line):
    temp = getData(location)
    return SimulationParams(float(temp[line][0]),float(temp[line][1]),float(temp[line][2]))

def getViewParams(location,line):
    temp = getData(location)
    return ViewParams(float(temp[line][0]),float(temp[line][1]),float(temp[line][2]))

def getParticles(location):
    temp = getData(location)
    temp.pop(0)
    particles = []
    for x in temp:
        particles.append(KinematicParticle(float(x[0]),Vector(float(x[1]),float(x[2])),Vector(float(x[3]),float(x[4]))))
    return particles





def simulateFile(paramLine,viewLine,particleFileName):
    #sets up the initial simulation contiditions, eg how long it will run ect
    simulationParams = getSimulationParams(dataLocation + "\\simulationParams.csv",paramLine)
    #sets up the UI
    viewParams = getViewParams(dataLocation + "\\viewParams.csv",viewLine)
    particles = getParticles(dataLocation + particleFileName)
    command = SimulateToFile(particles,simulationParams,viewParams,fileName,FPS)
    command.execute()

def simShowTest(paramLine,viewLine,particleFileName):
    #sets up the initial simulation contiditions, eg how long it will run ect
    simulationParams = getSimulationParams(dataLocation + "\\simulationParams.csv",paramLine)
    #sets up the UI
    viewParams = getViewParams(dataLocation + "\\viewParams.csv",viewLine)
    particles = getParticles(dataLocation + particleFileName)
    command = SimulateAndShow(particles,simulationParams,viewParams,'Circle')
    command.execute()
simShowTest(1,1,"\\particles.csv")
