import unittest

from graphism.node import Node
from graphism.graph import Graph

class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.graph = Graph()
        self.nodes = []
        for i in range(1000):
            n = Node()
            self.graph.add_node(n)
            self.nodes.append(n)
            
    def tearDown(self):
        self.graph = None
        self.nodes = None