import unittest
import random 
import time
import weakref

from graphism.tests import TestApi

from graphism.node import Node
from graphism.graph import Graph

import sys

class GraphTest(TestApi):
    
    def test_init(self):
        g = Graph([(1,2),(1,3),(1,4),(1,5)])
        
        one = g.get_node_by_name(1)
        two = g.get_node_by_name(2)
        three = g.get_node_by_name(3)
        four = g.get_node_by_name(4)
        five = g.get_node_by_name(5)
        
        assert one.degree() == 4
        for n in [two, three, four, five]:
            assert n.degree() == 1
        
        