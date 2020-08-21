class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y
class Particle:
    def __init__(self,mass,pos):
        self.m = mass
        self.pos = pos
#allows you to create a particle without first having to create a position
def particle(mass,x,y):
    return Particle(mass,Position(x,y))
    
#function that finds out what segment cors is in
#0 - top left, 1 - top right, 2 bottom left, 3 - bottom right
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
        #blank children nodes
        self.children = [None,None,None,None]
        #if there is only one particle in the node that particle is held here
        self.particle = None
    def addParticle(self,newParticle):
        #if there are no particles in this node put the particle in here
        if self.particleCount == 0:
            self.particle = newParticle
            """if there is another particle in this node then find the segmant
            that is goes in and add to node"""
        else:
            self.addToCorrectChild(newParticle)
            if self.particle != None:
                self.addToCorrectChild(self.particle)
                #wipe the particle as we now have multiple particles in the same node
                self.particle = None

        self.particleCount += 1

    def addToCorrectChild(self,particle):
        #find quadrent that the particle should go in 
        childIndex = quadrantNumber(particle.pos,self.midPoint)
        #if the child index is not occupied 
        if self.children[childIndex] == None:
            #calculate the width of the child
            childHalfWidth = self.halfWidth / 2.0
            """calculate the new childs midpoint by adding or subtracting the
            appropriate offsets"""
            deltaX = [-childHalfWidth, +childHalfWidth, -childHalfWidth, +childHalfWidth]
            deltaY = [-childHalfWidth, -childHalfWidth, +childHalfWidth, +childHalfWidth]
            #if segement is 0 then the x coordinate will 
            childX = deltaX[childIndex]+self.midPoint.x
            childY = deltaY[childIndex]+self.midPoint.y
            childMidpoint = Position(childX,childY)
            self.children[childIndex] = Node(childMidpoint ,childHalfWidth)
            
        self.children[childIndex].addParticle(particle)
