import sys 
import os
sys.path.append(os.path.abspath("../../main/python"))

from tree import *
import random

lst = [particle(1,-3,-3),particle(1,-2,-3)]

def buildTree(lst,rootNode):
    for x in range(len(lst)):
        rootNode.addParticle(lst[x])
    print(rootNode.children)
              
rootNode = Node(Position(0,0),5)
buildTree(lst,rootNode)

#change names at some point

