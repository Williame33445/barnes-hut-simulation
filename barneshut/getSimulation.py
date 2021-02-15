import sys
import os

sys.path.append(os.path.abspath("."))

from barneshut.simulationCommand import *
from barneshut.tree import *
from barneshut.particle import *
from barneshut.simulator import *
from barneshut.view import *

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


#1 is simulate to file, 2 is simulate and show
def barnesHutCLI(folderLocation,runType,fileName=""):
    simulationParams = getSimulationParams(folderLocation + "\\simulationParams.csv",1)
    viewParams = getViewParams(folderLocation + "\\viewParams.csv",1)
    particles = getParticles(folderLocation + "\\particles.csv")
    #if filename is 1 then the program is run atomaticaly
    if runType == 1:
        command = SimulateToFile(particles,simulationParams,viewParams,folderLocation+"\\"+fileName,FPS)
        command.execute()
    elif runType == 2:
        command = SimulateAndShow(particles,simulationParams,viewParams,'Circle')
        command.execute()
#fileName needs to be MP4

