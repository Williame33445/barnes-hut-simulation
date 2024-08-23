import numpy as np
import itertools
import csv
import sys
import os   
import matplotlib.pyplot as plt

w = np.array([0,0,1])
a = 2.5
b = 1.5

fileName = "C:\workspace\git-repos\\barnes-hut-simulation\\barneshut\data\spiral-galaxy\particles.csv" #generate particle directly in directory?

ellipse = []
with open(fileName,"w",newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Mass","PositionX","PositionY","VelocityX","VelocityY"])

    for i,j in itertools.product(range(-100,100), repeat=2):
        r = np.array([i,j])
        if r @ r <= 200:
            if (r[0]/a)**2 + (r[1]/b)**2 <= 1:
                line = [100,i,j]
                line += list(np.cross(w,np.array([i,j,0]))[:2])
                ellipse.append([i,j])
            else:
                line = [1,i,j]
                line += list((10**-7)*np.random.uniform(-1,1,2)) 
            csvwriter.writerow(line)

ellipse = np.array(ellipse)
plt.scatter(ellipse[:,0],ellipse[:,1])
plt.show()