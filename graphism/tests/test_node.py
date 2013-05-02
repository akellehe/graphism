import unittest
import random 
import time
import weakref

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

    def test_cleanup(self):
        target = Node()
        to_clean = [Node(), Node(), Node()]
        not_to_clean = [Node(), Node()]
        for n in to_clean + not_to_clean:
            random.choice([target.add_parent, target.add_child])(n)
            
        assert len(target.connections().keys()) == 5
        assert target.degree() == 5
        """
        for n in to_clean:
            to_clean.remove(n)
            del n
        
        print "connections: %s" % len(target.connections().keys())
        print "degree:      %s" % target.degree()
        
        assert len(target.connections().keys()) == 2
        assert target.degree() == 2
        """
    
    def test_weakref_cleanup(self):
        class A:
            pass
        
        a = A()
        refs = []
        def cleanup(wr):
            refs.remove(wr)
        
        refs.append(weakref.ref(a, cleanup))
        refs.append(weakref.ref(a, cleanup))
        refs.append(weakref.ref(a, cleanup))

        for ref in refs:
            assert ref() is a        
        
        del a
        
        assert len(refs) == 0
        

if __name__ == '__main__':
    unittest.main()
            