import sys
import pickle
import random

from graphism.node import Node
from graphism.edge import Edge
from graphism.vendor.priodict import priorityDictionary

from graphism.helpers import tp, rp, return_none_from_one

class Graph(object):
    """
    Takes an edge list of the form:

    .. code-block:: python
    
        [(1,2),(2,3),...(1,4)]
        
    Or of the form
    
    .. code-block:: python
    
        [{'parent': str,
          'child': str,
          'multiplicity': long,
          'weight': float},...]
    
    :param bool directed: If set to False the graph will be undirected and transmissions can occur from child-to-parent as well as parent-to-child
    :param function transmission_probability: The transmission probability function. Should take one argument of type graphism.edge.Edge and return a float on 0,1. 
    :param function recovery_probability: The recovery probability function. Should take a single object of type graphism.node.Node. Returns a float on [0,1] indicating the probability of recovery for the node.
    :param function infection: The callback function to execute when a new node is infected. Takes the node as the only argument. (type graphism.node.Node)
    :param function recovery: The callback function to execute when a node recovers from infection. Takes the node as the only argument. (type graphism.node.Node)
    
    """
    __nodes = None
    __edges = None
    
    __susceptible = None
    __infected = None
    __recovered = None
    
    __directed = None
    __transmission_probability = None
    __recovery_probability = None
    __infection = None
    __recovery = None
    __susceptibility = None
    __edgelist = None
    
    def _simple_init(self, edges):
        for parent, child in edges:
            self.add_edge(parent, child)
                
    def _complex_init(self, edges):
        for edge_metadata in edges:
            self.add_edge(**edge_metadata)
    
    def __init__(self, edges, directed=False, transmission_probability=None, recovery_probability=None, infection=None, recovery=None, susceptibility=None):
        self.__nodes = {}
        self.__edges = {}

        self.__susceptible = set([])
        self.__infected = set([])
        self.__recovered = set([])
        
        self.__directed = directed
        self.__transmission_probability = transmission_probability
        self.__recovery_probability = recovery_probability
        self.__infection = infection
        self.__recovery = recovery
        self.__susceptibility = susceptibility
        
        self.__edgelist = []
        
        if len(edges[0]) == 2: # For simple edge lists:
            self._simple_init(edges)
        else: # For full edge exports:
            self._complex_init(edges)

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

    def add_node(self, name):
        if name not in self.__nodes:
            self.__nodes[name] = Node(name, graph=self)

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
            
            self.__edgelist.append(edge)
            
            self.add_node(parent)
            self.add_node(child)
            
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
    
    def edges(self):
        """
        Returns a unique list of all the edges in the graph.
        
        :rtype list(graphism.edge.Edge):
        """
        return self.__edgelist
    
    def infected(self):
        """
        Returns a unique set of infected nodes
        
        :rtype set(graphism.node.Node):
        """
        return self.__infected

    def susceptible(self):
        """
        Returns a unique set of susceptible nodes
        
        :rtype set(graphism.node.Node):
        """
        return self.__susceptible
    
    def recovered(self):
        """
        Returns a unique set of recovered nodes
        
        :rtype set(graphism.node.Node):
        """
        return self.__recovered
    
    def propagate(self):
        """
        Iterates over all infected nodes and propagates an infection according to the probability of transmission function operating on each edge between that infected node and a susceptible node.
        
        :rtype None:
        """
        for node in self.__infected:
            edges = self.__edges[node.name]
            for child_name, edge in edges.items():
                if self.__transmission_probability(edge) <= random.random():
                    child = self.__nodes[child_name]
                    if child in self.__susceptible:
                        self.__susceptible.remove(child)
                        self.__infected.add(child)
                        child.infect()
                        
    def _infection(self):
        """
        Returns the infection callback
        """
        return self.__infection
    
    def _recovery(self):
        """
        Returns the recovery callback
        """           
        return self.__recovery
    
    def set_transmission_probability(self, tp):
        """
        Sets the transmission probability function for the graph.
        
        :param function tp: The transmission probability function. Takes an argument of type graphism.edge.Edge as the only argument. Returns a float on [0,1] indicating the probability of a transmission.
        
        """
        self.__transmission_probability = tp
        
    def set_recovery_probability(self, rp):
        """
        Sets the recovery probability function for the graph.
        
        :param function rp: The recovery probability function. Takes an argument of type graphism.node.Node as the only argument. Returns a float on [0,1] indicating the probability of a recovery.
        """
        self.__recovery_probability = rp
        
    def recover(self):
        """
        Iterates over infected nodes allowing them to recover according to their probability of recovery.
        
        """
        for node in self.__infected:
            if self.__recovery_probability(node) <= random.random():
                self.__infected.remove(node)
                self.__recovered.add(node)
                node.recover()
                
    def set_infection(self, infection):
        """
        Setter for the infection callback function. Executes on a node when it's infected.
        
        :param function infection: The infection callback
        """
        self.__infection = infection
        
    def set_recovery(self, recovery):
        """
        Setter for the recovery callback function. Executes on a node when it recovers.
        
        :param function recovery: The recovery callback
        """
        self.__recovery = recovery
        
    def set_susceptibility(self, susceptibility):
        """
        Sets the method to execute on a node to put it back in 'susceptible' state. e.g. If you decorated a node to indicate infection or recovery, you would clean it up here.
        
        :param function susceptibility: The function to execute on a node to indicate it is susceptible. Takes one argument of type graphism.node.Node
        """
        self.__susceptibility = susceptibility
        
    def reset(self):
        """
        Moves all infected and recovered nodes back to 'susceptible' state.
        
        """
        for node in list(self.__infected):
            self.__susceptibility(node)
            self.__infected.remove(node)
        for node in list(self.__recovered):
            self.__susceptibility(node)
            self.__recovered.remove(node)
            
    def infect_seeds(self, seed_nodes):
        """
        Infects the given set of seed nodes.
        
        :param list(graphism.node.Node) seed_nodes: The list of nodes to infect initially.
        """
        for node in seed_nodes:
            self.__infected.add(node)
            node.infect()
            
    def save(self, filepath):
        """
        Saves the graph to a file.
        
        """
        with open(filepath, 'w+') as f:
            pickle.dump(self, f)