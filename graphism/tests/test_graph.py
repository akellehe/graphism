import unittest
import random 
import time
import weakref

from graphism.tests import TestApi

from graphism.node import Node
from graphism.graph import Graph

import sys

class GraphTest(TestApi):
    
    def test_init_positional_edge(self):
        g = Graph([(1,2),(1,3),(1,4),(1,5)])
        
        one = g.get_node_by_name(1)
        two = g.get_node_by_name(2)
        three = g.get_node_by_name(3)
        four = g.get_node_by_name(4)
        five = g.get_node_by_name(5)
        
        assert one.degree() == 4, "Expected 4, got %s" % one.degree()
        for n in [two, three, four, five]:
            assert n.degree() == 1
        
    def test_init_advanced_defs(self):
        g = Graph(graph=[{'from_': 1,
                          'to_': 2,
                          'type_': 'first',
                          'weight_': 1.0
                         },{'from_': 1,
                          'to_': 3,
                          'type_': 'second',
                          'weight_': 2.0
                         },{'from_': 1,
                          'to_': 4,
                          'type_': 'third',
                          'weight_': 3.0
                         },{'from_': 1,
                          'to_': 5,
                          'type_': 'fourth',
                          'weight_': 4.0
                         }], 
                  directed=True,
                  transmission_probability=lambda x,y: 1.0)
        
        one = g.get_node_by_name(1)
        two = g.get_node_by_name(2)
        three = g.get_node_by_name(3)
        four = g.get_node_by_name(4)
        five = g.get_node_by_name(5)
        
        assert one.degree() == 4, "Expected 4, got %s" % one.degree()
        for n in [two, three, four, five]:
            assert n.degree() == 1
            
        assert one.edges()[2].type_ == 'first'
        assert one.edges()[3].type_ == 'second'
        assert one.edges()[4].type_ == 'third'
        assert one.edges()[5].type_ == 'fourth'

        assert one.edges()[2].weight_ == 1.0
        assert one.edges()[3].weight_ == 2.0
        assert one.edges()[4].weight_ == 3.0
        assert one.edges()[5].weight_ == 4.0
        
        

        