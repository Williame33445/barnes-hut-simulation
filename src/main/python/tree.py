class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def translated(self,offset):
        return Position(self.x+offset.x, self.y+offset.y)
    def scaled(self,factor):
        return Position(self.x*factor, self.y*factor)

class Particle:
    def __init__(self,mass,pos):
        self.m = mass
        self.pos = pos
    def __str__(self):
        #allows you to define what str() does for this class
        return ("center=(" + str(self.pos.x) + "," + str(self.pos.y) + "),mass="+ str(self.m))
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
        self.leafParticle = None
        self.mass = 0
        self.centerOfMass = Position(0,0)
    def addParticle(self,newParticle):
        #if there are no particles in this node put the particle in here
        if self.particleCount == 0:
            self.leafParticle = newParticle
        else:
            """if there are other particles in this node then find the segmant
            that is goes in and add to node"""
            #add particle to child node
            self.addToCorrectChild(newParticle)
            """this recusively runs untill untill we get to a leaf node(bottom node) and extends it
            until one bellow its own node"""
            if self.leafParticle != None:
                #does the same proccess as new particle until both particles have there own node
                self.addToCorrectChild(self.leafParticle)
                #wipe the particle as we now have multiple particles in the same node
                self.leafParticle = None

        self.particleCount += 1

    def addToCorrectChild(self,particle):
        #find quadrent that the particle should go in
        childIndex = quadrantNumber(particle.pos,self.midPoint)
        """if the child isn't occupied it returns none and calculates the childs midpoint and halfWidth
        otherwise it returns the values of the particles that occupy it"""
        child = self.getOrCreateChildAt(childIndex)
        """recursion then happens again and the entire proccess continues to happen until the particles
        each have there own node"""
        child.addParticle(particle)

    def getOrCreateChildAt(self, childIndex):
        #we define (0,0) at the center of the screen
        #if the child index is not occupied
        if self.children[childIndex] == None:
            #calculate the width of the child
            childHalfWidth = self.halfWidth / 2.0
            """calculate the new child's midpoint by adding or subtracting the
            appropriate offsets"""
            #are defined due to the way segments were defined
            deltaX = [-1, +1, -1, +1]
            deltaY = [-1, -1, +1, +1]
            #calculate an unscaled offset and then scale it
            offset = Position(deltaX[childIndex],deltaY[childIndex]).scaled(childHalfWidth)
            #translate position
            childMidpoint = self.midPoint.translated(offset)
            #define the child
            self.children[childIndex] = Node(childMidpoint ,childHalfWidth)
        return self.children[childIndex]

    def findMassDistribution(self):
        if self.particleCount == 1:
            self.mass = self.leafParticle.m
            self.centerOfMass = self.leafParticle.pos
        else:
            for c in filter(None, self.children):
                c.findMassDistribution()
                self.mass += c.mass
                self.centerOfMass = self.centerOfMass.translated(c.centerOfMass.scaled(c.mass))
            self.centerOfMass = self.centerOfMass.scaled(1.0/self.mass)
