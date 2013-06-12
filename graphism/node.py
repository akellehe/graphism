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

    def infect(self):
        """
        Executes the callback function on the node after it becomes infected.
        
        """
        self.graph._infection(self)
        
    def recover(self):
        """
        Executes the callback function on the node after it recovers
        
        """
        self.graph._recovery(self)