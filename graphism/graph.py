from graphism.node import Edge, Node

class Graph(object):
    
    __nodes = None
    __infected = None
    
    def __init__(self, *args, **kwargs):
        """
        Takes an edge list of the form:
        
        ..code-block::
        
             [dict, dict, dict...dict] 
        
        as the first positional argument where valid keys are from_, to_, type_,
        and weight_. Type and weight are optional.
        
        __init__ creates a node for each unique integer and adds the node to the graph.
        
        Possible keyword arguments are:
        
        :param bool directed: If set to False the graph will be undirected and transmissions can occur from child->parent as well as parent->child
        :param function transmission_probability: The transmission probability function. Should take two arguments of type graphism.node.Node. The first positional argument is the parent (infection host), the second is the child. 
        :param list(dict) graph: You can optionally pass the graph as a keyword argument instead of the first positional argument.
        
        """
        nodes = {}
        if 'graph' in kwargs:
            graph = kwargs['graph']
            for edge in graph:
                parent = edge['from_']
                child = edge['to_']
                type_ = edge.get('type_', None)
                weight_ = edge.get('weight_', 1.0)
                
                p = Node(name=parent, 
                         directed=kwargs.get('directed', False), 
                         transmission_probability=kwargs.get('tranmission_probability', None))
                c = Node(name=child,  
                         directed=kwargs.get('directed', False), 
                         transmission_probability=kwargs.get('tranmission_probability', None))
                
                p.add_child(c, type_=type_, weight_=weight_)
                
                nodes[parent] = p
                nodes[child] = c
        elif args:
            graph = args[0]
            for edge in graph:
                parent, child = edge
                p = Node(name=parent, 
                         directed=kwargs.get('directed', False),
                         transmission_probability=kwargs.get('transmission_probability', None))
                c = Node(name=child,
                         directed=kwargs.get('directed', False),
                         transmission_probability=kwargs.get('transmission_probability', None))
                p.add_child(c)
                nodes[parent] = p
                nodes[child] = c
                
        self.__infected = set([])    
        self.__nodes = set(nodes.items())
        self.__nodes_by_name = nodes
    
    def get_node_by_name(self, name):
        return self.__nodes_by_name.get(name, None)
    
    def add_node(self, node):
        """
        Adds a node to the graph.
        
        :param graphism.node.Node node: The node to add.
        """
        self.__nodes.add(node)
        
    def add_edge(self, from_, to_):
        """
        Adds an edge between two nodes in the graph.
        
        :param graphism.node.Node from_: The node to add an edge from. (parent)
        :param graphism.node.Node to_: The terminal node. (child)
        
        :rtype tuple(graphism.node.Node, graphism.node.Edge, graphism.node.Node: A tuple of the parent node, edge, and child node.
        """
        from_.add_child(to_)
        return (from_, from_.edges()[to_.name()], to_)
        
        
    def set_infection(self, callback):
        """
        Sets the infection function to func. Defines a wrapper to add the 
        to self.__infected before executing the defined callback

        :param function func: The function to infect with.
        
        :rtype None:
        """
        def i(node):
            self.__infected.add(node)
            callback(node)

        self.__infection = i
        
    def infect_seeds(self, seed_nodes):
        """
        Infects the seed_nodes.
        
        :param set(graphism.node.Node) seed_nodes: The nodes to start the infection with.
        """
        for n in seed_nodes:
            n.infect(self.__infection)
            
    def infected(self):
        """
        Returns the set of infected nodes in the graph.
        
        :rtype set(graphism.node.Node):
        """
        return self.__infected
    
    def susceptible(self):
        """
        Returns the set of susceptible nodes in the graph.
        
        :rtype set(graphism.node.Node):
        """
        return self.__nodes.difference(self.__infected)
    
    def propagate(self):
        """
        Executes the propagate (and recovery) function for each infected node 
        once.
        
        """
        for n in self.__infected:
            n.propagate()
    