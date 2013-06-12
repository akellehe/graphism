import unittest
import random 
import time
import weakref

from graphism.tests import TestApi

from graphism.node import Node
from graphism.edge import Edge
from graphism.graph import Graph
from graphism.helpers import tp, rp

import sys

class GraphTest(TestApi):
    
    def test_graph_init(self):
        edges = [(1,2),(2,3),(1,3),(1,4),(4,5)]
        
        g = Graph(edges)
        
        assert len(g.edges()) == 5, g.edges()
        assert len(g.nodes()) == 5, "Expected 5, got %s" % len(g.nodes())
    
        