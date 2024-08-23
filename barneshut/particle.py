import math 
import numpy as np

#newtonain case
global G
G = 6.67*10**-11

def A(p1,p2,m2):
    r = p1 - p2
    rMag = np.linalg.norm(r)
    if rMag == 0:
        return np.zeros(2)
    return -G*m2*r/rMag**3

#galaxy case
# global G
# G = 0.0001
# alpha = beta = 0.2 
# p = 2
# q = 4
# D = 1.4

# def A(p1,p2,m2):
#     r = p1 - p2
#     rMag = np.linalg.norm(r)
#     if rMag == 0:
#         return np.zeros(2)
    
#     if rMag > D:
#         return -G*m2*r/rMag**3
#     else:
#         return (-alpha/(rMag**p) + beta/(rMag**q))*m2*r/rMag


class Particle:
    def __init__(self,mass,pos):
        self.mass = mass
        self.pos = pos

    def __str__(self):
        #allows you to define what str() does for this class
        return "mass=" + str(self.mass) + ",centre=" + str(self.pos)
    
    def accelerationTowards(self,p):
        return A(self.pos,p.pos,p.mass)


#gives the initial state of the system
class KinematicParticle(Particle):
    def __init__(self,mass,pos,velocity):
        Particle.__init__(self,mass,pos)
        self.velocity = velocity

    def __str__(self):
        #allows you to define what str() does for this class
        return Particle.__str__(self) + ",velocity=" + str(self.velocity)

#allows you to create a particle without first having to create a position
def particle(mass,x,y):
    return Particle(mass,np.array([x,y]))

def kinematicParticle(mass,x,y,vx,vy):
    return KinematicParticle(mass,np.array([x,y]),np.array([vx,vy]))
    
def getCM(particles): 
    mass = 0
    centre = np.zeros(2)
    for p in particles:
        mass += p.mass
        centre += p.pos*p.mass
    centre /= mass

    return Particle(mass, centre)

