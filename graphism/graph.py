class Graph(object):
    
    __nodes = set([])
    __infected = set([])
    
    def add_node(self, node):
        """
        Adds a node to the graph.
        
        :param graphism.node.Node node: The node to add.
        """
        self.__nodes.add(node)
        
    def infection(self, func):
        """
        Sets the infection function to func.

        :param function func: The function to infect with.
        """
        def i(node):
            self.__infected.add(node)
            func(node)

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
    
    def add_edge(self, parent, child):
        """
        Adds a child and a parent connection to the graph.
        
        :param graphism.node.Node parent: The parent node.
        :param graphism.node.Node child: The child node.
        
        :rtype None
        """
        self.add_node(parent)
        self.add_node(child)
        
        parent.add_child(child)
        child.add_parent(parent)