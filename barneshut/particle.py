import math 
import numpy as np
global G
G = 6.67*10**-11


class Particle:
    def __init__(self,mass,pos):
        self.mass = mass
        self.pos = pos
    def __str__(self):
        #allows you to define what str() does for this class
        return "mass=" + str(self.mass) + ",centre=" + str(self.pos)
    def accelerationTowards(self,p):
        r = self.pos - p.pos
        rMag = np.linalg.norm(r)
        if rMag == 0:
            return np.zeros(2) #is this required
        return -G*p.mass*r/rMag**3


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


    
def combinedParticle(particles): #rename to Cm
    mass = 0
    centre = np.zeros(2)
    for p in particles:
        mass += p.mass
        centre += p.pos*p.mass
    centre = centre/mass
    return Particle(mass, centre)

