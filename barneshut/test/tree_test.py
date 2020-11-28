import unittest

from barneshut.tree import *

class TreeTest(unittest.TestCase):

    def test_EmptyRoot(self):
        rootNode = treeNode(midPoint=Vector(0.0,0.0),halfWidth=5.0)
        self.assertEqual(0.0, rootNode.midPoint.x)
        self.assertEqual(0.0, rootNode.midPoint.y)
        self.assertEqual(5.0, rootNode.halfWidth)
        self.assertEqual(0.0, rootNode.particleCount)
        # Check that there is no combinedParticle and there are no children
        self.assertEqual("{o[,,,]}", rootNode.structureAsString())


    def test_SimpleTree(self):
        rootNode = treeNode(midPoint=Vector(0.0,0.0),halfWidth=5.0)

        p1 = particle(1.0,-3.0,-3.0)
        rootNode.addParticle(p1)
        self.assertEqual(p1, rootNode.combinedParticle)
        self.assertEqual(1.0, rootNode.particleCount)
        self.assertEqual("{*[,,,]}", rootNode.structureAsString())

        p2 = particle(1.0,-2.0,-3.0)
        rootNode.addParticle(p2)
        self.assertIsNone(rootNode.combinedParticle)
        self.assertEqual(2.0, rootNode.particleCount)
        self.assertEqual("{o[{o[{*[,,,]},{*[,,,]},,]},,,]}", rootNode.structureAsString())

        topLeftChild = rootNode.childNodes[0]
        self.assertIsNotNone(topLeftChild)
        self.assertEqual(-2.5, topLeftChild.midPoint.x)
        self.assertEqual(-2.5, topLeftChild.midPoint.y)
        self.assertEqual(2.5, topLeftChild.halfWidth)
        self.assertEqual(2.0, topLeftChild.particleCount)
        self.assertIsNone(topLeftChild.combinedParticle)

        topLeftGrandChild = topLeftChild.childNodes[0]
        self.assertIsNotNone(topLeftGrandChild)
        self.assertEqual(-3.75, topLeftGrandChild.midPoint.x)
        self.assertEqual(-3.75, topLeftGrandChild.midPoint.y)
        self.assertEqual(1.25, topLeftGrandChild.halfWidth)
        self.assertEqual(1.0, topLeftGrandChild.particleCount)
        self.assertEqual(p1, topLeftGrandChild.combinedParticle)
       
        topRightGrandChild = topLeftChild.childNodes[1]
        self.assertIsNotNone(topRightGrandChild)
        self.assertEqual(-1.25, topRightGrandChild.midPoint.x)
        self.assertEqual(-3.75, topRightGrandChild.midPoint.y)
        self.assertEqual(1.25, topRightGrandChild.halfWidth)
        self.assertEqual(1.0, topRightGrandChild.particleCount)
        self.assertEqual(p2, topRightGrandChild.combinedParticle)


    def test_ParticlesAtSamePosition(self):
        rootNode = treeNode(midPoint=Vector(0.0,0.0),halfWidth=5.0,maxDepth=3)

        p1 = particle(1.0,-2.0,-3.0)
        rootNode.addParticle(p1)
        rootNode.addParticle(p1)
        self.assertEqual("{o[{o[,{o2},,]},,,]}", rootNode.structureAsString())

    def test_findMassDistribution_Branching(self):
        rootNode = newTestTreeWithTwoParticles(maxDepth=5)
        self.assertEqual("{o[,,,{o[{*[,,,]},{*[,,,]},,]}]}", rootNode.structureAsString())

        self.assertIsNone(rootNode.combinedParticle)
        rootNode.findMassDistribution()
        self.assertEquals("mass=4.0,centre=(16.0,8.0)",str(rootNode.combinedParticle))

    def test_findMassDistribution_NonBranching(self):
        rootNode = newTestTreeWithTwoParticles(maxDepth=1)
        self.assertEqual("{o2}", rootNode.structureAsString())

        self.assertIsNone(rootNode.combinedParticle)
        rootNode.findMassDistribution()
        self.assertEquals("mass=4.0,centre=(16.0,8.0)",str(rootNode.combinedParticle))

    # FIXME: Confirm these acceleration results

    def test_netAccelerationOf_Branching(self):
        rootNode = newTestTreeWithTwoParticles(maxDepth=5)
        self.assertEqual("{o[,,,{o[{*[,,,]},{*[,,,]},,]}]}", rootNode.structureAsString())
        rootNode.findMassDistribution()
        acceleration = rootNode.netAccelerationOf(ps)
        self.assertEquals(str(accelerationOfPsToP0AndP1),str(acceleration))

    def test_netAccelerationOf_BranchingCombined(self):
        rootNode = newTestTreeWithTwoParticles(maxDepth=5,theta=10)
        self.assertEqual("{o[,,,{o[{*[,,,]},{*[,,,]},,]}]}", rootNode.structureAsString())
        rootNode.findMassDistribution()
        acceleration = rootNode.netAccelerationOf(ps)
        self.assertEquals(str(accelerationOfPsToP0CombinedWithP1),str(acceleration))

    def test_netAccelerationOf_NonBranching(self):
        rootNode = newTestTreeWithTwoParticles(maxDepth=1)
        self.assertEqual("{o2}", rootNode.structureAsString())
        rootNode.findMassDistribution()
        acceleration = rootNode.netAccelerationOf(ps)
        self.assertEquals(str(accelerationOfPsToP0AndP1),str(acceleration))

p0=particle(mass=1.0,x=1.0,y=2.0)
p1=particle(mass=3.0,x=21.0,y=10.0)
ps=particle(2.0,0.0,0.0)
def newTestTreeWithTwoParticles(maxDepth,theta=0.01):
    rootNode = treeNode(midPoint=Vector(0.0,0.0),halfWidth=25.0,maxDepth=maxDepth,theta=theta)
    rootNode.addParticle(p0)
    rootNode.addParticle(p1)
    return rootNode

accelerationOfPsToP0 = ps.accelerationTowards(p0)
accelerationOfPsToP1 = ps.accelerationTowards(p1)

accelerationOfPsToP0AndP1 = accelerationOfPsToP0.plus(accelerationOfPsToP1)
accelerationOfPsToP0CombinedWithP1 = ps.accelerationTowards(combinedParticle([p0,p1]))