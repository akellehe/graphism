import sys

from graphism.node import Node
from graphism.edge import Edge
from graphism.vendor.priodict import priorityDictionary

from graphism.helpers import tp, rp, return_none_from_one

class Graph(object):
    """
    Takes an edge list of the form:

    .. code-block:: python
    
        [(1,2),(2,3),...(1,4)]


    as the first positional argument where valid keys are from_, to_, type_,
    and weight_. Type and weight are optional.
    
    __init__ creates a node for each unique integer and adds the node to the graph.
    
    Possible keyword arguments are:
    
    :param bool directed: If set to False the graph will be undirected and transmissions can occur from child-to-parent as well as parent-to-child
    :param function transmission_probability: The transmission probability function. Should take two arguments of type graphism.node.Node. The first positional argument is the parent (infection host), the second is the child. 
    :param function recovery_probability: The recovery probability function. Should take a single objet of type graphism.node.Node. Returns a float on [0,1] indicating the probability of recovery for the node.
    :param function infection: The callback function to execute when a new node is infected. Takes the node as the only argument.
    :param function recovery: The callback function to execute when a node recovers from infection. Takes the node as the only argument.
    :param list(dict) edges: You can optionally pass the graph as a keyword argument instead of the first positional argument.
    
    """
    __nodes = None
    __edges = None
    
    __susceptible = None
    __infected = None
    __recovered = None
    
    def _simple_init(self, edges):
        for parent, child in edges:
            self.add_edge(parent, child)
                
    def _complex_init(self, edges):
        for edge_metadata in edges:
            self.add_edge(**edge_metadata)
    
    def __init__(self, edges, directed=False, transmission_probability=None, recovery_probability=None, infection=None, recovery=None):
        self.__nodes = {}
        self.__edges = {}

        self.__susceptible = set([])
        self.__infected = set([])
        self.__recovered = set([])
        
        if len(edges[0]) == 2: # For simple edge lists:
            self._simple_init(edges, directed, transmission_probability, recovery_probability, infection, recovery)
        else: # For full edge exports:
            self._complex_init(edges, directed, transmission_probability, recovery_probability, infection, recovery)

    def edge(self, parent, child):
        """
        Returns an edge by the parent and child names
        
        :param str parent: The name of the parent node
        :param str child: The name of the child node
        
        :rtype graphism.edge.Edge: The edge or None if it does not exist
        """
        if parent in self.__edges and child in self.__edges[parent]:
            return self.__edges[parent][child]
        else:
            return None

    def add_edge(self, parent, child, weight=1.0, multiplicity=1L):
        """
        Adds an edge to the graph
        
        :param str parent: The name of the parent node.
        :param str child: The name of the child node
        :param float weight: The weight on the edge.
        :param long multiplicity: The multiplicity of the edge.
        
        :rtype graphism.edge.Edge: The edge added to the graph.
        """
        edge = self.edge(parent, child)
        if edge:
            edge.multiplicity += 1L
        else:
            edge = Edge(parent, child, multiplicity=multiplicity, weight=weight, graph=self)
            if parent not in self.__nodes:
                self.__nodes[parent] = Node(parent, graph=self)
            if child not in self.__nodes:
                self.__nodes[child] = Node(child, graph=self)
            if parent in self.__edges:
                self.__edges[parent][child] = edge
            else:
                self.__edges[parent] = {child: edge}
        return edge
        
    def nodes(self):
        """
        Returns a unique list of all the nodes in the graph.
        
        :rtype list(graphism.node.Node):
        """
        return self.__nodes.values()
