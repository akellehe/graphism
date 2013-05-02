import time
import random
import weakref
import sys

class Edge(object):
    """
    Represents a Edge between the node containing the Edge and a parent or child node.
    
    """
    node = None
    multiplicity = None
    type = None
    
    def __init__(self, origin=None, multiplicity=1L, type=None, dest=None):
        assert isinstance(origin, weakref.ref)
        assert isinstance(dest, weakref.ref)
        
        self.origin = origin                   
        self.dest = dest
        self.multiplicity = multiplicity
        self.type = type
        
        self.__origin_name = origin().name()
        self.__dest_name = dest().name()
        
        origin().add_edge(dest().name(), self)
        dest().add_edge(origin().name(), self)

class Node(object):
    """
    Represents a node in a graph.
    
    """
    __name = None
    __degree = 0L
    __parents = None
    __children = None
    __edges = None
    __propagation_function = None
    
    
    def __init__(self, parents=None, children=None, name=None, directed=False):
        """
        Instantiates a node in a graph. 
        
        :param list(graphism.node.Node) parents: A list of parent nodes. They are added as parents to this node.
        :param list(graphism.node.Node) children: A list of child nodes. They are added as children to this node.
        """
        self.__parents = set([])
        self.__children = set([])
        self.__edges = {}
        
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

    def add_edge(self, name, edge):
        if name in self.__edges:
            self.__edges[name].multiplicity += 0.5
        else:
            self.__edges[name] = edge
        self.degree(1L)

    def remove_all_edges_by_name(self, name):
        if name in self.__edges:
            edge = self.__edges.pop(name)
            self.degree(-1L*edge.multiplicity)

    def remove_parent_ref(self, wr):
        """
        Removes a weakref from the parent list.
        
        """
        self.__parents.remove(wr)
        
    def remove_child_ref(self, wr):
        """
        Removes a weakref from the child list.
        
        """
        self.__children.remove(wr)

    def add_parent(self, parent_node):
        """
        Adds a parent node to the set of parents. If the node already exists the 
        multiplicity of the node is increased.
        
        :rtype long: The multiplicity of the edge to parent_node.
        """
        node_name = parent_node.name()
        weakself = weakref.ref(self)
        def cleanup(wr):
            weakself().remove_parent_ref(wr) 
            weakself().remove_all_edges_by_name(node_name)
            
        self.__parents.add(weakref.ref(parent_node, cleanup))
        
        edge = Edge(origin=weakref.ref(parent_node), 
                    dest=weakref.ref(self))
                    
        return self.__edges[node_name].multiplicity
    
    def add_child(self, child_node):
        """
        Adds a child node to the set of children. If the node already exists the
        multiplicity of the node is increased.
        
        """
        node_name = child_node.name()
        weakself = weakref.ref(self)
        def cleanup(wr):
            weakself().remove_child_ref(wr) 
            weakself().remove_all_edges_by_name(node_name)
            
        self.__children.add(weakref.ref(child_node, cleanup))
        
        edge = Edge(origin=weakref.ref(self),
                    dest=weakref.ref(child_node))

        return self.__edges[node_name].multiplicity
        
    def edges(self):
        """
        Returns a dict of Edges associated with this node.
        
        :rtype dict(str, graphism.node.Edge):
        """
        return self.__edges

    def degree(self, to_add=None):
        """
        Returns the current degree of the node.
        
        :rtype long:
        """
        if to_add:
            self.__degree += to_add
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
        
        conn = self.__edges[to_node.name()]
        multiplicity = conn.multiplicity
        degree = self.degree()
        if degree == 0L:
            return 0L
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
