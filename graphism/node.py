import time
import random
import weakref

from graphism.edge import Edge
from graphism.helpers import return_none, tp, rp

class Node(object):
    """
    Represents a node in a graph.
    
    """
    children = set([])
    parents = set([])
