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

class EdgeTest(TestApi):
    
    def test_to_dict(self):
        parent = Node()
        child = Node()
        multiplicity = 2
        type_ = 'test'
        weight_ = 2.0
        directed = True
        length = lambda e: e.weight_
        
        e = Edge(weakref.ref(parent), weakref.ref(child), multiplicity, type_, weight_, directed, length)
        e_d = e.to_dict()
        
        assert e_d['from_'] == parent.name()
        assert e_d['to_'] == child.name()
        assert e_d['multiplicity'] == multiplicity
        assert e_d['type_'] == type_
        assert e_d['weight_'] == weight_
        assert e_d['directed'] == directed
        assert e_d['length'] == length
        
        e = Edge(weakref.ref(parent), weakref.ref(child))
        e_d = e.to_dict()
        
        assert e_d['from_'] == parent.name()
        assert e_d['to_'] == child.name()
        assert e_d['multiplicity'] == 1L
        assert e_d['weight_'] == 1.0
        assert e_d['length'](e) == 1.0
        assert e_d['type_'] == None
        assert e_d['directed'] == False 