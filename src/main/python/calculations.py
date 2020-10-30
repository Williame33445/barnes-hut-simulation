global g
g = 6.67*10**-11

def calculateGravitationalForce(particle1,particle2):
    #we are assuming that the force is being calculated from particle1
    r = particle1.pos.findDistance(particle2)
    magnitude = (G)*(particle1.mass)*(particle2.mass)/(r**3)
    #gives vector in the direction of the
    direction = particle2.pos.translate(particle1.pos.scaled(-1))
    return Force(magnitude,direction)

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def translated(self,offset):
        return Position(self.x+offset.x, self.y+offset.y)
    def scaled(self,factor):
        return Position(self.x*factor, self.y*factor)
    def findDistance(self,pos2):
        return sqrt((self.x-pos2.x)**2+(self.y-pos2.y)**2)

class Particle:
    def __init__(self,mass,pos):
        self.m = mass
        self.pos = pos
    def __str__(self):
        #allows you to define what str() does for this class
        return ("centre=(" + str(self.pos.x) + "," + str(self.pos.y) + "),mass="+ str(self.m))
#allows you to create a particle without first having to create a position
def particle(mass,x,y):
    return Particle(mass,Position(x,y))

class Vector:
    def __init__(self,magnitude,direction):
        self.vector = direction.translate(magnitude)

class Velocity(Vector):
    def __init__(self,magnitude,direction):
        Vector.__init__(self,magnitude,direction)
class Force(Vector):
    def __init__(self,magnitude,direction):
        Vector.__init__(self,magnitude,direction)
        #will just deduce acceleration from this
