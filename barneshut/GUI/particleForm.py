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
        self.getFolderLocation =  getFolderLocation
        self.pack()
        #Entry(self, width=10, fg='blue', font=('Arial',16,'bold'))
        self.table = Table(self.getParticles(),self)

    def getParticles(self):
        particles = self.getData(0)
        particles.pop(0)
        kinematicParticles = []
        for x in particles:
            kinematicParticles.append(KinematicParticle(float(x[0]),Vector(float(x[1]),float(x[2])),Vector(float(x[3]),float(x[4]))))
        return kinematicParticles

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