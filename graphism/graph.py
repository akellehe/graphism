from graphism.node import Node
from graphism.edge import Edge

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
    :param list(dict) graph: You can optionally pass the graph as a keyword argument instead of the first positional argument.
    
    """
    
    __nodes = None
    __infected = None
    __transmission_probability = None
    __recovery_probability = None
    __infection = None
    __recovery = None
    
    def __init__(self, *args, **kwargs):
        self.__nodes = {}
        self.__infected = {}        
        self.__transmission_probability = tp
        self.__recovery_probability = rp
        
        if 'graph' in kwargs:
            self.__init_nodes_from_kwargs(kwargs)
        elif args:
            self.__init_nodes_from_args(args, kwargs)
            
        self.set_infection(return_none_from_one)
        self.set_recovery(return_none_from_one)
    
    def add_edge_by_node_sequence(self, parent, child, directed=None, transmission_probability=None, type_=None, weight_=1.0, recovery_probability=None):
        """
        Creates nodes and an edge between two nodes for a given name.
        
        :param str parent: The name for the parent node
        :param str child: The name for the child node
        :param bool directed: Whether or not the edge should be directed.
        :param function transmission_probability: The transmission probability function associated with the edge.
        :param str type_: The type of edge
        :param str weight_: The weight of the edge
        """
        p = self.get_node_by_name(parent)
        if not p:
            p = Node(name=parent,
                     transmission_probability=transmission_probability or self.__transmission_probability,
                     recovery_probability=recovery_probability or self.__recovery_probability,
                     graph=self)

        c = self.get_node_by_name(child)
        if not c:
            c = Node(name=child,
                     transmission_probability=transmission_probability or self.__transmission_probability,
                     recovery_probability=recovery_probability or self.__recovery_probability,
                     graph=self)
        
        p.add_child(c, type_=type_, weight_=weight_)
        
        self.add_node(p)
        self.add_node(c)
    
    def __init_nodes_from_kwargs(self, kwargs):
        """
        Initializes internal nodes for a set of keyword arguments.
        
        :param dict kwargs: The keyword arguments for the __init__ method.
        
        """
        graph = kwargs['graph']
        directed = kwargs.get('directed', False)
        transmission_probability=kwargs.get('transmission_probability', None)
        
        for edge in graph:
            parent = edge['from_']
            child = edge['to_']
            type_ = edge.get('type_', None)
            weight_ = edge.get('weight_', 1.0)
            
            self.add_edge_by_node_sequence(parent, child, directed, transmission_probability, type_, weight_)
        
    def __init_nodes_from_args(self, args, kwargs):
        """
        Initializes internal nodes for a set of positional and keyword arguments.
        
        :param tuple args: The positional arguments for the __init__ method.
        :param dict kwargs: The keyword arguments for the __init__ method.
        
        """
        graph = args[0]
        for edge in graph:
            parent, child = edge
            self.add_edge_by_node_sequence(parent, child)
    
    def get_node_by_name(self, name):
        """
        Searches the internal dict maintaining the ONLY strong reference to internal nodes by name. Returns the node with that name.
        
        :param str name: The name of the node to return.
        
        :rtype graphism.node.Node:
        """
        return self.__nodes.get(name, None)
    
    def add_node(self, node):
        """
        Adds a node to the graph.
        
        :param graphism.node.Node node: The node to add.
        
        :rtype graphism.node.Node: 
        """
        if node.name() not in self.__nodes:
            self.__nodes[node.name()] = node
        return node
        
    def add_edge(self, from_, to_):
        """
        Creates an edge between two nodes in the graph.
        
        :param graphism.node.Node from_: The node to add an edge from. (parent)
        :param graphism.node.Node to_: The terminal node. (child)
        
        :rtype tuple(graphism.node.Node, graphism.node.Edge, graphism.node.Node: A tuple of the parent node, edge, and child node.
        """
        if from_ not in self.__nodes:
            self.add_node(from_)
        if to_ not in self.__nodes:
            self.add_node(to_)
            
        from_.add_child(to_)
        
        return (from_, from_.edges()[to_.name()], to_)
        
        
    def set_infection(self, callback):
        """
        Sets the infection function to callback. Should return True if the node was infected. False otherwise.

        :param function callback: The function to execute on a node being infected. The only argument should be the node itself.
        
        :rtype None:
        """
        self.__infection = callback
        
    def set_recovery(self, callback):
        """
        Sets the recovery function to callback. Should return True if the node recovers. False otherwise

        :param function callback: The function to execute on a node being infected. The only argument should be the node itself.
        
        :rtype None:
        """           
        self.__recovery = callback
        
    def infect_seeds(self, seed_nodes):
        """
        Infects the seed_nodes by executing the infect method for those nodes.
        
        :param set(graphism.node.Node) seed_nodes: The nodes to start the infection with.
        """
        for n in seed_nodes:
            n.infect(self.__infection)
            
    def infected(self):
        """
        Returns the set of infected nodes in the graph.
        
        :rtype set(graphism.node.Node):
        """
        return set(self.__infected.values())
    
    def add_infected(self, node):
        """
        Adds a node to the list of infected nodes
        
        """
        self.__infected[node.name()] = node
        
    def remove_infected(self, node):
        """
        Removes a node form the list of infected nodes
        
        """
        if node.name() in self.__infected:
            del self.__infected[node.name()]
    
    def nodes(self):
        """
        Returns the internal nodes as a set.
        
        :rtype set(graphism.node.Node):
        """
        return set(self.__nodes.values())
    
    def susceptible(self):
        """
        Returns the set of susceptible nodes in the graph.
        
        :rtype set(graphism.node.Node):
        """
        return self.nodes().difference(self.infected())
    
    def propagate(self):
        """
        First recovers infected nodes according to the probability of recovery. 
        Second, propagates infections from infected nodes according to the probability of transmission. 
        
        """
        self.recover()
            
        for n in self.infected():
            n.propagate_infection(self.__infection)
            
    def recover(self):
        """
        Executes the recovery function for each infected node and subsequently 
        removes it from the 'infected' set iff that node recovered.
        
        """
        for n in self.infected():
            n.recover(self.__recovery) # Returns true if recovered, false if not

    