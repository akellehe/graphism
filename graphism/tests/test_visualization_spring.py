import unittest
import random 
import time
import weakref

from graphism.tests import TestApi

from graphism.node import Node
from graphism.edge import Edge
from graphism.graph import Graph
from graphism.visualization import spring

import sys

class VisualizationSpringTest(TestApi):
    
    def test_initialize_positions(self):
        g = Graph([(1,2),(1,3),(1,4),(1,5)])
        
        spring.initialize_positions(g)
        
        for node in g.nodes():
            assert node.velocity, "Expected velocity attribute to be set"
            assert isinstance( node.velocity, list ), "Expected velocity to be a list"
            assert len(node.velocity) == 2, "Expected velocity list to have two entries"
            assert isinstance(node.velocity[0], float), "Expected x-velocity to be a float"
            assert isinstance(node.velocity[1], float), "Expected y-velocity to be a float"
            
            assert node.position, "Expected position attribute to be set"
            assert isinstance(node.position, list), "Expected position to be a list"
            assert len(node.position) == 2, "Expected position list to have two entries"
            assert isinstance(node.position[0], float), "Expected x-position to be a float"
            assert isinstance(node.position[1], float), "Expected y-position to be a float"
                        

    def test_calculate_forces(self):
        g = Graph([(1,2),(1,3)])

        for n in g:
            for e in n.edges().values():
                e.weight_ = 0.5
                    
        spring.initialize_positions(g)
        
        g[1].position = [0,0]
        g[2].position = [1,0]
        g[3].position = [0,1]
         
        spring.calculate_forces(g)
                
        assert g[1].forces == [0.5, 0.5], "Expected 4,4. Got %s" % g[1].forces
        
        assert ("%0.2f" % g[2].forces[0]) == "-1.21", "%0.2f" % g[2].forces[0]
        assert ("%0.2f" % g[2].forces[1]) == "0.71", "%0.2f" % g[2].forces[1]
        
        assert ("%0.2f" % g[3].forces[0]) == "0.71", "%0.2f" % g[3].forces[0]
        assert ("%0.2f" % g[3].forces[1]) == "-1.21", "%0.2f" % g[3].forces[1]

    def test_layout(self):
        g = Graph([(1,2),(1,3)])
        
        for n in g:
            for e in n.edges().values():
                e.weight_ = 0.5
                
        spring.layout(g)