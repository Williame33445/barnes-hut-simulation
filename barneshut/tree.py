from barneshut.calculations import *
global theta
theta = 5

"""function that finds out what segment cors is in
0 - top left, 1 - top right, 2 bottom left, 3 - bottom right"""
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
        self.childNodes = [None,None,None,None]
        self.combinedParticle = None
    def mass(self):
        return self.combinedParticle.mass
    def centreOfMass(self):
        return self.combinedParticle.pos
    def children(self):
        return filter(None,self.childNodes)
    def isLeaf(self):
        if self.particleCount == 1:
            return True
    def addParticle(self,newParticle):
        #if there are no particles in this node put the particle in here
        if self.particleCount == 0:
            self.combinedParticle = newParticle
        else:
            """if there are other particles in this node then find the segment
            that the new prticle goes in and add to node"""
            #add particle to child node
            self.addToCorrectChild(newParticle)
            """this recusively runs until we get to a leaf node(bottom node) and extends it
            until one bellow its own node"""
            if self.isLeaf():
                #does the same proccess for the existing particle until both particles have their own node
                self.addToCorrectChild(self.combinedParticle)
                #wipe the particle as we now have multiple particles in the same node
                self.combinedParticle = None

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
        #we define (0,0) at the centre of the screen
        #if the child index is not occupied
        if self.childNodes[childIndex] == None:
            #calculate the width of the child
            childHalfWidth = self.halfWidth / 2.0
            """calculate the new child's midpoint by adding or subtracting the
            appropriate offsets"""
            #are defined due to the way segments were defined
            deltaX = [-1, +1, -1, +1]
            deltaY = [-1, -1, +1, +1]
            #calculate an unscaled offset and then scale it
            offset = Vector(deltaX[childIndex],deltaY[childIndex]).scaled(childHalfWidth)
            childMidpoint = self.midPoint.translated(offset)
            #define the child
            self.childNodes[childIndex] = Node(childMidpoint ,childHalfWidth)
        return self.childNodes[childIndex]

    def findMassDistribution(self):
        #if the object is a leaf then no calculations are required
        if self.isLeaf():
            return
        mass = 0
        centreOfMass = zeroVector()
        for c in self.children():
            #recursively runs find mass distribtion through the children of the nodes to find mass and center of mass
            c.findMassDistribution()
            mass += c.mass()
            centreOfMass = centreOfMass.translated(c.centreOfMass().scaled(c.mass()))
        centreOfMass = centreOfMass.scaled(1.0/mass)
        self.combinedParticle = Particle(mass, centreOfMass)

    def calculateNetAcceleration(self,targetParticle):
        force = zeroVector()
        r = self.centreOfMass().findDistance(targetParticle.pos)
        d = self.halfWidth * 2
        if self.isLeaf() or (d/r < theta):
            force = self.combinedParticle.calculateAcceleration(targetParticle)
        else:
            for c in self.children():
                force = force.translated(c.calculateNetAcceleration(targetParticle))
        return force
