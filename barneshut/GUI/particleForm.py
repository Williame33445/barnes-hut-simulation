import tkinter as tk
import csv
import sys
import os
from tkinter.constants import LEFT
import copy

sys.path.append(os.path.abspath("."))

from barneshut.view import *

from barneshut.simulator import *
from barneshut.GUI.table import *
from barneshut.particle import *

class ParticleForm(tk.LabelFrame):
    def __init__(self,parent,BG,getFolderLocation):
        super().__init__(parent,bg =BG,text="Particles")
        #this contains the intial state of particles not the latest state from the simulator
        self.particles = []
        self.getFolderLocation =  getFolderLocation
        self.pack()
        self.table = Table(self.particles,self)
        self.layout()

    def loadParticles(self):
        particlesFromFile = self.getData()
        self.particles.clear()
        for x in particlesFromFile:
            self.particles.append(KinematicParticle(float(x[0]),np.array([float(x[1]),float(x[2])]),np.array([float(x[3]),float(x[4])])))
        self.table.refresh()

    def saveParticles(self):
        with open(self.getFolderLocation() + "/particles.csv","w",newline="") as file:
            file.truncate()
            writer = csv.writer(file)
            writer.writerow(self.table.parameters)
            writer.writerows(self.table.getAllData())

    def getData(self):
        data = []
        with open(self.getFolderLocation() + "/particles.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        data.pop(0)
        return data

    def newParticles(self):
        #creates deep copy of particles because this form holds the intial state of particles which we 
        # don't want updated by the simulation(if we just returned self.particles the simulator would have a
        # pointer to the initial state of particles)
        return copy.deepcopy(self.particles)

    def layout(self):
        tk.Button(self,text="Load",command=self.loadParticles).grid(row=self.table.rows()+1, column=0)
        tk.Button(self,text="Save",command=self.saveParticles).grid(row=self.table.rows()+1, column=1)

