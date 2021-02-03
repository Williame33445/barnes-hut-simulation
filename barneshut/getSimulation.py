import sys
import os

sys.path.append(os.path.abspath("."))

from barneshut.simulationCommand import *
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *

dataLocation = "C:\\workspace\\git-repos\\barnes-hut-simulation\\barneshut\\data"
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
    return SimulationParams(float(temp[line][0]),float(temp[line][1]),float(temp[line][2]),float(temp[line][3]),float(temp[line][4]))

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

def getFileName(location):
    temp = getData(location)
    return temp[1][3]


def barnesHutCLI(folderLocation):
    simulationParams = getSimulationParams(folderLocation + "\\simulationParams.csv",1)
    viewParams = getViewParams(folderLocation + "\\viewParams.csv",1)
    particles = getParticles(folderLocation + "\\particles.csv")
    fileName = getFileName(folderLocation + "\\viewParams.csv")
    #if filename is 1 then the program is run atomaticaly
    if fileName != "1":
        command = SimulateToFile(particles,simulationParams,viewParams,folderLocation+"\\"+fileName,FPS)
        command.execute()
    else:
        command = SimulateAndShow(particles,simulationParams,viewParams,'Circle')
        command.execute()
barnesHutCLI("C:\\workspace\\git-repos\\barnes-hut-simulation\\barneshut\\data\\data1")


