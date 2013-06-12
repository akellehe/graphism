import time
import random
import weakref

from graphism.edge import Edge
from graphism.helpers import return_none, tp, rp

class Node(object):
    """
    Represents a node in a graph.
    
    """
    children = None
    parents = None
    name = None
    
    def __init__(self, name, graph=None):
        self.name = name
        self.graph = graph
        self.children = set([])
        self.parents = set([])
