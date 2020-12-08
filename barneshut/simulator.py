from barneshut.particle import zeroVector
from barneshut.tree import treeNode
from dataclasses import dataclass

class Simulator:

    def __init__(self,particles,halfWidth):
        self.particles = particles
        self.halfWidth = halfWidth

    def buildTree(self):
        self.rootNode = treeNode(zeroVector(),self.halfWidth)
        self.addParticles()
        self.rootNode.findMassDistribution()

    def addParticles(self):
        for p in self.particles:
            self.rootNode.addParticle(p)

    def netAccelerationOf(self,particle):
        return self.rootNode.netAccelerationOf(particle)

    def applyAcceleration(self,timeElapsed):
        accelerations = [self.netAccelerationOf(p) for p in self.particles]
        for x in range(len(self.particles)):
            acceleration = accelerations[x]
            deltaVelocity = acceleration.times(timeElapsed)
            self.particles[x].velocity.translate(deltaVelocity)

    def applyVelocity(self,timeElapsed):
        for p in self.particles:
            deltaPosition = p.velocity.times(timeElapsed)
            p.pos.translate(deltaPosition)

    def tick(self,timeElapsed):
        self.buildTree()
        self.applyVelocity(timeElapsed)
        self.applyAcceleration(timeElapsed)

@dataclass
class SimulationParams:
    halfWidth: float
    tickPeriod: float
    totalDuration: float

    def numberOfCycles(self):
        return int(self.totalDuration/self.tickPeriod)

    def width(self):
        return 2.0 * self.halfWidth

def simulate(particles,params,onTick):
    simulator = Simulator(particles,params.halfWidth)

    for t in range(params.numberOfCycles()):
        simulator.tick(params.tickPeriod)

        continueSimulation = onTick(t)
        if not continueSimulation:
            break
