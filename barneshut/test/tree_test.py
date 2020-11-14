import unittest

from barneshut.tree import *

class TreeTest(unittest.TestCase):

    def test_EmptyRoot(self):
        rootNode = Node(Vector(0.0,0.0),5.0)
        self.assertEqual(0.0, rootNode.midPoint.x)
        self.assertEqual(0.0, rootNode.midPoint.y)
        self.assertEqual(5.0, rootNode.halfWidth)
        self.assertEqual(0.0, rootNode.particleCount)
        for c in rootNode.childNodes:
            self.assertIsNone(c)
        for c in rootNode.children():
            self.fail('There should be no children')


    def test_SimpleTree(self):
        def checkChildrenExistFor(parent, childExists):
            for i in range(4):
                self.assertEqual(parent.childNodes[i]!=None, childExists[i], 'index ' + str(i))
        def checkNoChildrenExistFor(parent):
            checkChildrenExistFor(parent, [False, False, False, False])

        rootNode = Node(Vector(0.0,0.0),5.0)

        p1 = particle(1.0,-3.0,-3.0)
        rootNode.addParticle(p1)
        self.assertEqual(p1, rootNode.combinedParticle)
        self.assertEqual(1.0, rootNode.particleCount)
        checkNoChildrenExistFor(rootNode)

        p2 = particle(1.0,-2.0,-3.0)
        rootNode.addParticle(p2)
        self.assertIsNone(rootNode.combinedParticle)
        self.assertEqual(2.0, rootNode.particleCount)

        checkChildrenExistFor(rootNode, [True, False, False, False])

        topLeftChild = rootNode.childNodes[0]
        self.assertIsNotNone(topLeftChild)
        self.assertEqual(-2.5, topLeftChild.midPoint.x)
        self.assertEqual(-2.5, topLeftChild.midPoint.y)
        self.assertEqual(2.5, topLeftChild.halfWidth)
        self.assertEqual(2.0, topLeftChild.particleCount)
        self.assertIsNone(topLeftChild.combinedParticle)
        checkChildrenExistFor(topLeftChild, [True, True, False, False])

        topLeftGrandChild = topLeftChild.childNodes[0]
        self.assertIsNotNone(topLeftGrandChild)
        self.assertEqual(-3.75, topLeftGrandChild.midPoint.x)
        self.assertEqual(-3.75, topLeftGrandChild.midPoint.y)
        self.assertEqual(1.25, topLeftGrandChild.halfWidth)
        self.assertEqual(1.0, topLeftGrandChild.particleCount)
        self.assertEqual(p1, topLeftGrandChild.combinedParticle)
        checkNoChildrenExistFor(topLeftGrandChild)
       
        topRightGrandChild = topLeftChild.childNodes[1]
        self.assertIsNotNone(topRightGrandChild)
        self.assertEqual(-1.25, topRightGrandChild.midPoint.x)
        self.assertEqual(-3.75, topRightGrandChild.midPoint.y)
        self.assertEqual(1.25, topRightGrandChild.halfWidth)
        self.assertEqual(1.0, topRightGrandChild.particleCount)
        self.assertEqual(p2, topRightGrandChild.combinedParticle)
        checkNoChildrenExistFor(topRightGrandChild)
