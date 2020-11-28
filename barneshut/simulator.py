from barneshut.particle import zeroVector
from barneshut.tree import treeNode

class Simulator:

    def __init__(self,particles,halfWidth,maxDepth=15,theta=0.01):
        self.particles = particles
        self.halfWidth = halfWidth
        self.maxDepth = maxDepth
        self.theta = theta

    def buildTree(self):
        self.rootNode = treeNode(zeroVector(),self.halfWidth,self.maxDepth,self.theta)
        self.addParticles()
        self.rootNode.findMassDistribution()

    def addParticles(self):
        for p in self.particles:
            self.rootNode.addParticle(p)

    def netAccelerationOf(self,particle):
        return self.rootNode.netAccelerationOf(particle)

    def accelerations(self):
        accs = []
        for p in self.particles:
            accs.append(self.netAccelerationOf(p))
        return accs

    def applyAcceleration(self,timeElapsed):
        accs = self.accelerations()
        for x in range(len(self.particles)):
            deltaVelocity = accs[x].times(timeElapsed)
            self.particles[x].velocity.translate(deltaVelocity)

    def applyVelocity(self,timeElapsed):
        for p in self.particles:
            deltaPosition = p.velocity.times(timeElapsed)
            p.pos.translate(deltaPosition)

    def tick(self,timeElapsed):
        self.buildTree()
        self.applyVelocity(timeElapsed)
        self.applyAcceleration(timeElapsed)