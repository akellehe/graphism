import unittest
import random 
import time
import weakref

from graphism.tests import TestApi

from graphism.node import Node
from graphism.edge import Edge
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
        g = Graph(edges=[{'from_': 1,
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
        
    def test_get_node_by_name(self):
        g = Graph([(1,2),(1,3),(1,4),(1,5)])

        one = g.get_node_by_name(1)
        two = g.get_node_by_name(2)
        three = g.get_node_by_name(3)
        four = g.get_node_by_name(4)
        five = g.get_node_by_name(5)

        assert one.name() == 1
        assert two.name() == 2
        assert three.name() == 3
        assert four.name() == 4
        assert five.name() == 5

    def test_add_edge(self):
        g = Graph([(1,2),(1,3),(1,4),(1,5)])
        
        one = g.get_node_by_name(1)
        two = g.get_node_by_name(2)
        three = g.get_node_by_name(3)
        
        assert one.degree() == 4
        assert two.degree() == 1
        assert three.degree() == 1
        
        g.add_edge(one, two)
        
        assert one.degree() == 5
        assert two.degree() == 2
        assert three.degree() == 1
        
        g.add_edge(two, one)
        
        assert one.degree() == 6
        assert two.degree() == 3
        assert three.degree() == 1
        
        g.add_edge(two, three)
        
        assert one.degree() == 6
        assert two.degree() == 4
        assert three.degree() == 2
        
    def test_set_infection(self):
        g = Graph([(1,2),(1,3),(1,4),(1,5)])
        infected = []
        
        def callback(n):
            infected.append(n)
            
        g.set_infection(callback)
        
        one = g.get_node_by_name(1)
        two = g.get_node_by_name(2)
        three = g.get_node_by_name(3)
        
        g.infect_seeds([one, two, three])
        
        assert one in infected
        assert two in infected
        assert three in infected
        
        assert one in g.infected()
        assert two in g.infected()
        assert three in g.infected()
        
    def test_set_recovery(self):
        edges = []
        for i in range(1,100):
            for j in range(1,100):
                if i == j:
                    continue
                else:
                    edges.append((i,j))
                    
        g = Graph(edges)        

        recovered = []
        def recovery_function(n):
            recovered.append(n)
        
        g.set_recovery(recovery_function)

        g.infect_seeds([g.get_node_by_name(i) for i in range(1,100)])

        assert not recovered

        before = g.infected()
        g.recover()
        after = g.infected()
        
        assert not not recovered
        
        assert len(after) < len(before)        
    
    def test_set_transmission_function_in_constructor(self):
        
        target = [False]
        def trans(a,b):
            target[0] = True
            return 1
            
        g = Graph([(1,2)], 
                  transmission_probability=trans)
        
        g.infect_seeds([g.get_node_by_name(1)])
        
        g.propagate()
        
        assert target[0]
        
    def test_node_iterator(self):
        g = Graph([(1,2),(1,3),(1,4),(2,3)])        
        
        nodes = []
        at_two = []
        
        for n in g[1]:
            assert isinstance(n, Node)
            nodes.append(n)
            
        for n in g[2]:
            at_two.append(n)
            
        assert len(at_two) == 2, "Expected %s Got %s" % (1, len(at_two))
        assert len(nodes) == 3
        
    def test_graph_iterator(self):
        g = Graph([(1,2),(1,3),(1,4)]) 
        
        nodes = []
        
        for n in g:
            assert isinstance(n, Node)
            nodes.append(n)
            
        assert len(nodes) == 4
        
    def test_closeness(self):
        g = Graph([(1,2),(2,3),(3,4)]) 
        
        one = g[1]
        four = g[4]            
        
        closeness, path = g.closeness(one, four)
        assert closeness == 3.0

        g = Graph([(1,2),(2,3),(3,4)],
                  length=lambda e: e.weight_/2.0)
        
        one = g[1]
        four = g[4]
        
        closeness, path = g.closeness(one, four)
        
        assert closeness == 1.5
        
        
            
        