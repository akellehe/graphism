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
        self.graph = Graph()
        self.nodes = []
        for i in range(1000):
            n = Node()
            self.graph.add_node(n)
            self.nodes.append(n)
        assert len(self.nodes) == len(set(self.nodes))
        assert len(self.nodes) == 1000
        assert len(set([n.name() for n in self.nodes])) == 1000
        
        node = self.nodes[0]
        assert type('') == type(node.name())
        
        
    def test_add_parent_and_child(self):
        parent = Node()
        child = Node()
        
        parent.add_child(child)
        child.add_parent(parent)
        
        assert parent.is_parent_of(child)
        assert child.is_child_of(parent)
        
        assert parent.name() in child.edges()
        assert child.name() in parent.edges()
        
        assert parent.degree() == 2L
        assert child.degree() == 2L
        
        parent = Node()
        child = Node()
        parent.add_child(child)
        
        assert parent.degree() == 1L
        assert child.degree() == 1L
        
        assert child.is_child_of(parent)
        assert parent.is_parent_of(child)
        
    def test_degree(self):
        graph = Graph()
        nodes = []
        for i in range(1000):
            n = Node()
            graph.add_node(n)
            nodes.append(n)
        target = nodes[0]
        for n in nodes[1:]:
            random.choice([target.add_child, target.add_parent])(n)
        assert target.degree() == 999
    
    def test_edges(self):
        target = Node()
        to_add = [Node() for i in range(1000)]
        for n in to_add:
            random.choice([target.add_child, target.add_parent])(n)
        assert len(target.edges().keys()) == target.degree()

    def test_cleanup(self):
        target = Node()
        to_clean = [Node(), Node(), Node()]
        not_to_clean = [Node(), Node()]
        for n in to_clean + not_to_clean:
            random.choice([target.add_parent, target.add_child])(n)
            
        assert len(target.edges().keys()) == 5
        assert target.degree() == 5

        while to_clean:
            n = to_clean.pop()
            del n
                
        assert len(target.edges().keys()) == 2
        assert target.degree() == 2, "Actual degree is %s" % target.degree()
    
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

    def test_circular_weakref_cleanup(self):
        class A:
            pass
        class B:
            def __init__(self, a, b):
                self.a = a
                self.b = b
        a = A()
        b = A()
        
        refs = []
        
        def cleanup(wr):
            refs.remove(wr)
        
        a.b = weakref.ref(b, cleanup)
        b.a = weakref.ref(a, cleanup)
    
        br = B(weakref.ref(a), weakref.ref(b))
        
        refs.append(a.b)
        refs.append(b.a)
        
        assert len(refs) == 2
        
        del a
        
        assert len(refs) == 1
    
    def test_circular_node_cleanup(self):
        parent = Node()
        child = Node()
        
        par_mul = parent.add_child(child)
        assert par_mul == 1L, "Expected multiplicity 1, got %s" % par_mul
        child_mul = child.add_parent(parent) 
        assert child_mul == 2L, "Expected multiplicity 2, got %s" % child_mul
        
        assert parent.degree() == 2L, "Expected 2, got %s" % parent.degree()
        assert child.degree() == 2L, "Expected 2, got %s" % child.degree()
        
        del child
        
        assert len(parent.edges().items()) == 0, "Parent has %s edges." % len(parent.edges().items())
        assert parent.degree() == 0L, "Parent degree is: %s" % parent.degree()
        
        parent = Node()
        child = Node()
        
        assert parent.add_child(child) == 1L
        assert child.add_parent(parent) == 2L
        
        assert parent.degree() == 2L
        assert child.degree() == 2L
        
        del parent
        
        assert child.degree() == 0L, "Child degree is: %s" % child.degree()
        
    

if __name__ == '__main__':
    unittest.main()
            