import csv

def getDataline(location):
    data = []
    with open(location, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def getSimulationParams(location,line):
    temp = getData(location)
    return SimulationParams(temp[line]][0],temp[line][1],temp[line][2])

def getViewParams(location,line):
    temp = getData(location)
    return ViewParams(temp[line][0],temp[line][1],temp[line][2])

def getParticles(location):
    return getData(location,line)
        
