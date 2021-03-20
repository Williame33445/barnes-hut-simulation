import tkinter as tk
import csv
import sys
import os
from tkinter.constants import LEFT

sys.path.append(os.path.abspath("."))

from barneshut.view import *

from barneshut.simulator import *
from barneshut.GUI.table import *
from barneshut.particle import *

class ParticleForm(tk.LabelFrame):
    def __init__(self,parent,BG,getFolderLocation):
        super().__init__(parent,bg =BG,text="Particles")
        #giving particles by reference
        self.particles = []
        self.getFolderLocation =  getFolderLocation
        self.pack()
        self.loadParticles()
        self.table = Table(self.particles,self)

    def loadParticles(self):
        particlesFromFile = self.getData(0)
        particlesFromFile.pop(0)
        self.particles.clear()
        for x in particlesFromFile:
            self.particles.append(KinematicParticle(float(x[0]),Vector(float(x[1]),float(x[2])),Vector(float(x[3]),float(x[4]))))

    def getData(self,line):
        data = []
        with open(self.getFolderLocation() + "/particles.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        if line == 0:
            return data
        else:
            return data[line]

    def getParticles(self):
        return self.particles