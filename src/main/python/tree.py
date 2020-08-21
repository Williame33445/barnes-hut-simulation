
xm = 300
ym = 300
class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y
class Particle:
    def __init__(self,mass,pos):
        self.m = mass
        self.pos = pos

def particle(mass,x,y):
    return Particle(mass,Position(x,y))
    

def quadrantNumber(cors,midpoint):
    if (midpoint.x>cors.x)and(midpoint.y>cors.y):
        return 0
    elif (midpoint.x<=cors.x)and(midpoint.y>cors.y):
        return 1
    elif (midpoint.x>cors.x)and(midpoint.y<=cors.y):
        return 2
    else:
        return 3

class Node:
    def __init__(self,midPoint,halfWidth):
        self.midPoint = midPoint
        self.halfWidth = halfWidth
        self.particleCount = 0
        self.children = [None,None,None,None]
        self.particle = None
    def insertToNode(self,newParticle):
        if self.particleCount == 0:
            self.particle = newParticle
        else:
            self.addToCorrectChild(newParticle)
            if self.particle != None:
                self.addToCorrectChild(self.particle)

        self.particleCount += 1

    def addToCorrectChild(self,particle):
        childIndex = quadrantNumber(particle.pos,self.midPoint)
        if self.children[childIndex] == None:
            childHalfWidth = self.halfWidth / 2.0
            xChildCentres = [-childHalfWidth, +childHalfWidth, -childHalfWidth, +childHalfWidth]
            yChildCentres = [-childHalfWidth, -childHalfWidth, +childHalfWidth, +childHalfWidth]
            childX = xChildCentres[childIndex]+self.midPoint.x
            childY = yChildCentres[childIndex]+self.midPoint.y
            childMidpoint = Position(childX,childY)
            self.children[childIndex] = Node(childMidpoint ,childHalfWidth)
            
        self.children[childIndex].insertToNode(particle)
