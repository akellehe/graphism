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

    def __getattr__(self, key):
        return self.graph.edge_dict()[self.name][key]
        
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.name = state.get('name', None)
        self.graph = state.get('graph', None)
        self.children = state.get('children', set([]))
        self.parents = state.get('parents', set([]))

    def infect(self):
        """
        Executes the callback function on the node after it becomes infected.
        
        """
        self.graph.infection()(self)
        
    def recover(self):
        """
        Executes the callback function on the node after it recovers
        
        """
        self.graph.recovery()(self)
        
    def degree(self):
        """
        Returns the number of outgoing edges.
        
        """
        return long(self.graph.get_degree(self.name))
