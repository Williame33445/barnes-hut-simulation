import sys
import os
sys.path.append(os.path.abspath("src/main/python"))

from tree import *


def printTree(t,depth=0):
    print(depth*" " + "center=(" + str(t.midPoint.x)+","+str(t.midPoint.y)+")" + ",halfWidth=" +
    str(t.halfWidth) + ",numberOfChildren=" + str(t.particleCount-1))
    for c in filter(None,t.children):
        printTree(c,depth+1)


lst = [particle(1.0,-3.0,-3.0),particle(1.0,-2.0,-3.0)]

def buildTree(lst,rootNode):
    for x in range(len(lst)):
        rootNode.addParticle(lst[x])
    printTree(rootNode)

rootNode = Node(Position(0,0),5)
buildTree(lst,rootNode)
rootNode.findMassDistribution()
print(rootNode.combinedParticle)
# print(str(particle(1,2,3)))
#need to clean up
"""Next things to do:
-  add comments
- try and clean up more(tree and testing)
- proper testing(take from old calculator program)
- isLeaf function to make it cleaner(replaces self.particle count == 1)
- rename children to sectors and write function that takes out the nones"""
