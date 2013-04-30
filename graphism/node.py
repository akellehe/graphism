import time
import random
import weakref

class Connection(object):
    """
    Represents a connection between the node containing the connection and a parent or child node.
    
    """
    node = None
    multiplicity = 0
    type = None
    
    def __init__(self, node=None, multiplicity=0L, type=None, cleanup=lambda x: None):
        
        self.node = weakref.ref(node, cleanup)
        self.multiplicity = multiplicity
        self.type = type
        

class Node(object):
    """
    Represents a node in a graph.
    
    """
    __name = None
    __degree = 0L
    __parents = None
    __children = None
    __connections = None
    __propagation_function = None
    
    
    def __init__(self, parents=None, children=None, name=None, directed=False):
        """
        Instantiates a node in a graph. 
        
        :param list(graphism.node.Node) parents: A list of parent nodes. They are added as parents to this node.
        :param list(graphism.node.Node) children: A list of child nodes. They are added as children to this node.
        """
        self.__parents = set([])
        self.__children = set([])
        self.__connections = {}
        
        if parents:
            for p in parents:
                self.add_parent(p)
        if children:
            for c in children:
                self.add_child(c)
        if name:
            self.__name = name
        else:
            self.__name = str(random.random()) + str(time.time())
           
    
    def name(self):
        """
        Returns the node's name
        
        """
        return self.__name

    def __get_cleanup_callback(self, node):
        """
        Returns a callback that cleans up local references to the given node when it is 
        cleaned up.
        
        :param graphism.graph.node.Node node: The node to clean up.
        
        :rtype function:
        """
        def cleanup(wr): 
            conn = self.__connections.pop(node.name())
            self.__degree -= node.degree()
            if conn.type == 'parent':
                self.__parents.remove(wr)
            elif conn.type == 'child':
                self.__children.remove(wr)
        return cleanup

    def __add_connection(self, name, conn):
        if name in self.__connections:
            self.__connections[name].multiplicity += 1L
        else:
            self.__connections[name] = conn
            
        self.__degree += 1L

    def add_parent(self, parent_node):
        """
        Adds a parent node to the set of parents. If the node already exists the 
        multiplicity of the node is increased.
        
        :rtype long: The multiplicity of the node.
        """
        self.__parents.add(weakref.ref(parent_node))
        conn = Connection(node=parent_node, 
                          multiplicity=1L, 
                          type='parent', 
                          cleanup=self.__get_cleanup_callback(parent_node))

        self.__add_connection(parent_node.name(), conn)
                    
        return self.__connections[parent_node.name()].multiplicity
        
    def connections(self):
        """
        Returns a dict of connections associated with this node.
        
        :rtype dict(str, graphism.node.Connection):
        """
        return self.__connections
        
    def add_child(self, child_node):
        """
        Adds a child node to the set of children. If the node already exists the
        multiplicity of the node is increased.
        
        """
        self.__children.add(weakref.ref(child_node))
        conn = Connection(node=child_node,
                          multiplicity=1L,
                          type='child',
                          cleanup=self.__get_cleanup_callback(child_node))
            
        self.__add_connection(child_node.name(), conn)
        
        return self.__connections[child_node.name()].multiplicity
    
    def degree(self):
        """
        Returns the current degree of the node.
        
        :rtype long:
        """
        return self.__degree
    
    def infect(self, propagation_function=None):
        """
        Gets or sets the propagation function on the node. This is analogous to infecting the node. 
        
        :param function propagation_function: When passed it sets the function to infect other nodes.
        
        """
        if propagation_function:
            self.__propagation_function = propagation_function
            propagation_function(self)
        return self.__propagation_function
        
    def propagate(self, l=None):
        """
        Propagates the lambda function (executes the function on) nodes 
        at random in the set of parents and children weighted by the 
        probability of transmission to the nodes in those sets.
        
        The lambda is executed on the node it propagates to.
        
        :param lambda l: The function to propagate. It must take the node as the first argument
        """
        if l:
            if self.directed:
                nodes = self.__children
            else:
                nodes = self.__parents.union(self.__children)
                
            for n in nodes:
                probability = self.transmission_probability(n)
                if random.random() < probability:
                    n.infect(l) # It transmits!
            
    def transmission_probability(self, to_node, probability_function=None):
        """
        Returns the probability of transmission from self to to_node.
        
        :param graphism.node.Node to_node: The node we're transmitting the lambda to
        :param lambda probability_function: An optional probability function. It will be passed from_node, to_node.
        
        :rtype float: A floating point number less than 1
        """
        if probability_function:
            return probability_function(self, to_node)
        
        conn = self.__connections[to_node.name()]
        multiplicity = conn.multiplicity
        degree = self.degree()
        if degree == 0:
            return 0
        else:
            return multiplicity / degree
        
    def is_child_of(self, node):
        """
        Test whether or not self is a child node of node.
        
        :param graphism.node.Node node: The potential parent.
        
        :rtype bool:
        """
        return weakref.ref(node) in self.__parents
    
    def is_parent_of(self, node):
        """
        Test whether or not self is a parent node of node.
        
        :param graphism.node.Node node: The potential child.
        
        :rtype bool:
        """
        return weakref.ref(node) in self.__children