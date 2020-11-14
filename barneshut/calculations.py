import math 
global g
g = 6.67*10**-11

def calculateGravitationalForce(particle1,particle2):
    #we are assuming that the force is being calculated from particle1
    r = particle1.pos.findDistance(particle2.pos)
    if r==0:
        return Vector(0.0, 0.0)
    magnitude = (g)*(particle1.mass)*(particle2.mass)/(r**3)
    #gives vector in the direction of the
    direction = particle2.pos.translated(particle1.pos.scaled(-1))
    return direction.scaled(magnitude)

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def translated(self,offset):
        return Vector(self.x+offset.x, self.y+offset.y)
    def scaled(self,factor):
        return Vector(self.x*factor, self.y*factor)
    def findDistance(self,pos2):
        return math.sqrt((self.x-pos2.x)**2+(self.y-pos2.y)**2)

class Particle:
    def __init__(self,mass,pos):
        self.mass = mass
        self.pos = pos
    def __str__(self):
        #allows you to define what str() does for this class
        return ("centre=(" + str(self.pos.x) + "," + str(self.pos.y) + "),mass="+ str(self.mass))

#gives the initial state of the system
class KinematicParticle(Vector):
    def __init__(self,mass,pos,velocity):
        Particle.__init__(self,mass,pos)
        self.velocity = velocity

#allows you to create a particle without first having to create a position
def particle(mass,x,y):
    return Particle(mass,Vector(x,y))