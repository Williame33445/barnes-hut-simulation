from barneshut.tree import treeNode
import numpy as np

#Class that deals with running the simulation
class Simulator:

    def __init__(self,particles,halfWidth,theta,maxDepth):
        #list of all particles 
        self.particles = particles
        #half width of the range that we are thinking about
        self.halfWidth = halfWidth
        self.theta = theta
        self.maxDepth = maxDepth

    #creates the tree
    def buildTree(self):
        self.rootNode = treeNode(np.zeros(2),self.halfWidth,self.maxDepth,self.theta)
        self.addParticles()
        self.rootNode.findMassDistribution()

    #adds all particles
    def addParticles(self):
        for p in self.particles:
            self.rootNode.addParticle(p)
            
    #finds acceleration of a single particle
    def netAccelerationOf(self,particle):
        return self.rootNode.netAccelerationOf(particle)

    #cycles through rebuilding the tree and applying the velocities
    def tick(self,timeElapsed):
        self.buildTree()
        currentAccelerations = [self.netAccelerationOf(p) for p in self.particles]
        currentVelocities = [p.velocity for p in self.particles]
        for i in range(len(self.particles)): #i=j could be done better (just set to 0 here)
            self.particles[i].pos += currentVelocities[i]*timeElapsed 
            self.particles[i].velocity += currentAccelerations[i]*timeElapsed


#Class the controls how long the program runs for
class SimulationParams:
    def __init__(self,halfWidth,tickPeriod,totalDuration,theta,maxDepth):
        self.halfWidth = halfWidth
        self.tickPeriod = tickPeriod
        self.totalDuration = totalDuration
        self.theta = theta
        self.maxDepth = maxDepth

    def numberOfCycles(self):
        return int(self.totalDuration/self.tickPeriod)

    def width(self):
        return 2.0 * self.halfWidth
