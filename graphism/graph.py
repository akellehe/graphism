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
    _nodes = None
    _edges = None
    
    _susceptible = None
    _infected = None
    _recovered = None
    
    _directed = None
    _transmission_probability = None
    _recovery_probability = None
    _infection = None
    _recovery = None
    _susceptibility = None
    _edgelist = None
    
    def _simple_init(self, edges):
        for parent, child in edges:
            self.add_edge(parent, child)
                
    def _complex_init(self, edges):
        for edge_metadata in edges:
            self.add_edge(**edge_metadata)
            
    def __getitem__(self, key):
        return self._nodes[key]
    
    def _getstate(self):
        return {'_nodes': self._nodes,
                '_edges': self._edges,
                '_susceptible': self._susceptible,
                '_infected': self._infected,
                '_recovered': self._recovered,
                '_directed': self._directed,
                '_transmission_probability': self._transmission_probability,
                '_recovery_probability': self._recovery_probability,
                '_infection': self._infection,
                '_susceptibility': self._susceptibility,
                '_edgelist': self._edgelist }
    
    def __init__(self, edges, directed=False, transmission_probability=None, recovery_probability=None, infection=None, recovery=None, susceptibility=None):
        self._nodes = {}
        self._edges = {}

        self._susceptible = set([])
        self._infected = set([])
        self._recovered = set([])
        
        self._directed = directed
        self._transmission_probability = transmission_probability or tp
        self._recovery_probability = recovery_probability or rp
        self._infection = infection or return_none_from_one
        self._recovery = recovery or return_none_from_one
        self._susceptibility = susceptibility or return_none_from_one
        
        self._undirected_reciprocals = {} # Reciprocal edges for undirected graphs.
        
        self._edgelist = []
        
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
        if parent in self._edges and child in self._edges[parent]:
            return self._edges[parent][child]
        else:
            return None

    def add_node(self, name):
        if name not in self._nodes:
            node = Node(name, graph=self)
            self._nodes[name] = node
            self._susceptible.add(node)

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
            
            self._edgelist.append(edge)
            
            self.add_node(parent)
            self.add_node(child)
            
            if parent in self._edges:
                self._edges[parent][child] = edge
            else:
                self._edges[parent] = {child: edge}
        
        if not self._directed:
            recip = Edge(child, parent, multiplicity=multiplicity, weight=weight, graph=self)
            if child in self._undirected_reciprocals:
                self._undirected_reciprocals[child][parent] = recip
            else:
                self._undirected_reciprocals[child] = {parent: edge}
                        
        return edge
        
    def nodes(self):
        """
        Returns a unique list of all the nodes in the graph.
        
        :rtype list(graphism.node.Node):
        """
        return self._nodes.values()
    
    def edge_dict(self):
        """
        Returns the lookup dictionary for edges
        
        :rtype dict(str=>dict(str=>graphism.edge.Edge)):
        """
        return self._edges
    
    def edges(self):
        """
        Returns a unique list of all the edges in the graph.
        
        :rtype list(graphism.edge.Edge):
        """
        return self._edgelist
    
    def infected(self, infected=None):
        """
        Returns a unique set of infected nodes
        
        :rtype set(graphism.node.Node):
        """
        if infected:
            self._infected = infected
        return self._infected

    def susceptible(self, susceptible=None):
        """
        Returns a unique set of susceptible nodes
        
        :rtype set(graphism.node.Node):
        """
        if susceptible:
            self._susceptible = susceptible
        return self._susceptible
    
    def recovered(self, recovered=None):
        """
        Returns a unique set of recovered nodes
        
        :rtype set(graphism.node.Node):
        """
        if recovered:
            self._recovered = recovered
        return self._recovered
    
    def propagate(self):
        """
        Iterates over all infected nodes and propagates an infection according to the probability of transmission function operating on each edge between that infected node and a susceptible node.
        
        :rtype None:
        """
        for parent in list(self._infected):
            edges = self._edges[parent.name]
            if not self._directed:
                edges.update(self._undirected_reciprocals[parent.name])
            for child_name, edge in edges.items():
                prob = self._transmission_probability(edge)
                if random.random() <= prob:
                    child = self._nodes[child_name]
                    if child in self._susceptible:
                        self._susceptible.remove(child)
                        self._infected.add(child)
                        child.infect()
                        
    def infection(self):
        """
        Returns the infection callback
        """
        return self._infection
    
    def recovery(self):
        """
        Returns the recovery callback
        """           
        return self._recovery
    
    def set_transmission_probability(self, tp):
        """
        Sets the transmission probability function for the graph.
        
        :param function tp: The transmission probability function. Takes an argument of type graphism.edge.Edge as the only argument. Returns a float on [0,1] indicating the probability of a transmission.
        
        """
        self._transmission_probability = tp
        
    def set_recovery_probability(self, rp):
        """
        Sets the recovery probability function for the graph.
        
        :param function rp: The recovery probability function. Takes an argument of type graphism.node.Node as the only argument. Returns a float on [0,1] indicating the probability of a recovery.
        """
        self._recovery_probability = rp
        
    def recover(self):
        """
        Iterates over infected nodes allowing them to recover according to their probability of recovery.
        
        """
        for node in list(self._infected):
            if random.random() <= self._recovery_probability(node):
                self._infected.remove(node)
                self._recovered.add(node)
                node.recover()
                
    def set_infection(self, infection):
        """
        Setter for the infection callback function. Executes on a node when it's infected.
        
        :param function infection: The infection callback
        """
        self._infection = infection
        
    def set_recovery(self, recovery):
        """
        Setter for the recovery callback function. Executes on a node when it recovers.
        
        :param function recovery: The recovery callback
        """
        self._recovery = recovery
        
    def set_susceptibility(self, susceptibility):
        """
        Sets the method to execute on a node to put it back in 'susceptible' state. e.g. If you decorated a node to indicate infection or recovery, you would clean it up here.
        
        :param function susceptibility: The function to execute on a node to indicate it is susceptible. Takes one argument of type graphism.node.Node
        """
        self._susceptibility = susceptibility
        
    def reset(self):
        """
        Moves all infected and recovered nodes back to 'susceptible' state.
        
        """
        for node in list(self._infected):
            self._susceptibility(node)
            self._infected.remove(node)
            self._susceptible.add(node)
        for node in list(self._recovered):
            self._susceptibility(node)
            self._recovered.remove(node)
            self._susceptible.add(node)
            
    def infect_seeds(self, seed_nodes):
        """
        Infects the given set of seed nodes.
        
        :param list(graphism.node.Node) seed_nodes: The list of nodes to infect initially.
        """
        for node in seed_nodes:
            if node in self._susceptible:
                self._susceptible.remove(node)
            elif node in self._recovered:
                self._recovered.remove(node)
            elif node in self._infected:
                raise Exception("Attempting to infect an already infected node.")
            
            self._infected.add(node)
            node.infect()
            
    def save(self, filepath):
        """
        Saves the graph to a file.
        
        """
        with open(filepath, 'w+') as f:
            pickle.dump(self, f)
            
    def load(self, filepath):
        """
        Loads the graph from a file.
        
        """
        with open(filepath, 'rb') as f:
            target = pickle.load(f)
            state = target._getstate()
            for k, v in state.items():
                setattr(self, k, v)
                
    def add_graph(self, subgraph):
        """
        Adds a subgraph to the existing graph. If a node exists in subgraph not in self, it is created. If a node exists in subgraph as well as self the edges are added. If there are duplicate edges in subgraph, the edges in self have their multiplicity increased.
        
        :param graphism.graph.Graph subgraph: The subgraph to add to the existing graph.
        
        :rtype None:
        """
        for edge in subgraph.edges():
            self.add_edge(**edge.to_dict())
            
    
            
    def get_degree(self, node_name):
        degree = 0L
        edges = self._edges[node_name]
        if not self._directed:
            edges.update(self._undirected_reciprocals[node_name])
        for name, edge in edges.items():
            print edge
            degree += edge.multiplicity
        if not self._directed:
            return degree / 2L
        return degree
