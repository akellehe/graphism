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
    
    def test_simple_init(self):
        edges = [(1,2),(2,3),(1,3),(1,4),(4,5)]
        
        g = Graph(edges)
        
        assert len(g.edges()) == 5, g.edges()
        assert len(g.nodes()) == 5, "Expected 5, got %s" % len(g.nodes())
        
    def test_complex_init(self):
        edges = [{'parent': 1,
                  'child': 2,
                  'weight': 2.0,
                  'multiplicity': 2L},
                 {'parent': 2,
                  'child': 3,
                  'weight': 2.0,
                  'multiplicity': 2L},
                 {'parent': 1,
                  'child': 3,
                  'weight': 2.0,
                  'multiplicity': 2L},
                 {'parent': 1,
                  'child': 4,
                  'weight': 2.0,
                  'multiplicity': 2L},
                 {'parent': 4,
                  'child': 5,
                  'weight': 2.0,
                  'multiplicity': 2L}]
        
        g = Graph(edges)
        
        assert len(g.edges()) == 5
        assert len(g.nodes()) == 5
        
    def test_edge(self):
        edges = [(1,2),(2,3),(1,3),(1,4),(4,5)]
        
        g = Graph(edges)
        
        one_two_first = g.edge(1,2)
        one_two_second = g.edge(1,2)
        
        assert one_two_first is one_two_second
        
        none = g.edge(100,100)
        
        assert none is None
        
    def test_infect_seeds(self):
        edges = [(1,2),(2,3),(1,3),(1,4),(4,5)]
        
        g = Graph(edges)
        
        assert len(g.nodes()) == 5
        assert len(g.edges()) == 5
        assert len(g.infected()) == 0
        assert len(g.susceptible()) == 5
        assert len(g.recovered()) == 0
        
        g.infect_seeds([g[1],g[2]])
        
        assert len(g.susceptible()) == 3
        assert len(g.infected()) == 2
        assert len(g.recovered()) == 0
        
    def test_propagate(self):
        edges = []
        for i in range(100):
            for j in range(100):
                if i == j:
                    continue
                edges.append((i,j))
        g = Graph(edges)
        
        g.infect_seeds([g[0]])
        
        g.propagate()
        
        assert len(g.infected()) > 35 and len(g.infected()) < 65, len(g.infected())
        assert len(g.susceptible()) > 35 and len(g.susceptible()) < 65, len(g.susceptible())
        
    def test_recovery(self):
        edges = []
        for i in range(100):
            for j in range(100):
                if i == j:
                    continue
                edges.append((i,j))
        g = Graph(edges)
        
        g.infect_seeds([g[i] for i in range(100)])
        
        g.recover()
        
        assert len(g.infected()) > 35 and len(g.infected()) < 65, len(g.infected())
        assert len(g.recovered()) > 35 and len(g.recovered()) < 65, len(g.recovered())
        
    def test_reset(self):
        edges = []
        for i in range(100):
            for j in range(100):
                if i == j:
                    continue
                edges.append((i,j))
                
        g = Graph(edges)
        
        g.infect_seeds([g[i] for i in range(5)])
        
        g.propagate()
        g.recover()
        
        assert len(g.infected()) > 0
        assert len(g.recovered()) > 0
        
        g.reset()
        
        assert len(g.susceptible()) == 100, len(g.susceptible())        