import unittest
import random 

from graphism.tests import TestApi

from graphism.node import Node
from graphism.graph import Graph

import sys

class NodeTest(TestApi):

    def test_node_naming(self):
        assert len(self.nodes) == len(set(self.nodes))
        assert len(self.nodes) == 1000
        assert len(set([n.name() for n in self.nodes])) == 1000
        
        node = self.nodes[0]
        assert type('') == type(node.name())
        
        
    def test_add_parent_and_child(self):
        parent = self.nodes[0]
        child = self.nodes[1]
        
        parent.add_child(child)
        child.add_parent(parent)
        
        assert parent.is_parent_of(child)
        assert child.is_child_of(parent)
        
        assert parent.name() in child.connections()
        assert child.name() in parent.connections()
        
    def test_degree(self):
        target = self.nodes[0]
        for n in self.nodes[1:]:
            random.choice([target.add_child, target.add_parent])(n)
        assert target.degree() == 999
    
    def test_connections(self):
        target = Node()
        to_add = [Node() for i in range(1000)]
        for n in to_add:
            random.choice([target.add_child, target.add_parent])(n)
        assert len(target.connections().keys()) == target.degree()
