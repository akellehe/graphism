import time
import random
import weakref

from graphism.edge import Edge
from graphism.helpers import return_none, tp, rp

class Node(object):
    """
    Represents a node in a graph.
    
    """
    __name = None
    __degree = 0L
    __parents = None
    __children = None
    __edges = None
    __infection_function = None
    __transmission_probability = None
    __recovery_probability = None
    __recovery_function = None
    __graph = None
    
    def __init__(self, parents=None, children=None, name=None, transmission_probability=None, recovery_probability=None, graph=None):
        """
        Instantiates a node in a graph. 
        
        :param list(graphism.node.Node) parents: A list of parent nodes. They are added as parents to this node.
        :param list(graphism.node.Node) children: A list of child nodes. They are added as children to this node.
        :param str name: The name of the node. Must be unique for each node in the graph.
        :param function transmission_probability: Takes two arguments of type graphism.node.Node. The first positional argument is the parent node, the second is the child. The output should be the probability of an infection transmitting from the parent to the child over one exposure. The output should be a float in [0,1].
        """
        self.__parents = set([])
        self.__children = set([])
        self.__edges = {}
        
        self.__transmission_probability = transmission_probability or tp
        self.__recovery_probability = recovery_probability or rp
        
        self.__graph = return_none
        if graph:
            self.__graph = weakref.ref(graph)
        
        if parents:
            for p in parents:
                self.add_parent(p)
        if children:
            for c in children:
                self.add_child(c)
                
        if name is not None:
            self.__name = name
        else:
            self.__name = str(random.random()) + str(time.time())
    
    def name(self):
        """
        Returns the node's name
        
        """
        return self.__name

    def add_edge(self, name, edge):
        """
        Add an edge to the node. If the edge already exists the multiplicity is increased (by 0.5).

        :param str name: The name of the other node in the edge.
        :param graphism.node.Edge edge: The edge object.
        """
        if name in self.__edges:
            self.__edges[name].multiplicity += 0.5
        else:
            self.__edges[name] = edge
        self.degree(1L)

    def remove_all_edges_by_name(self, name):
        """
        Removes all edges in the graph associated with the node named name.
        
        :param str name: The name of the node to remove all edges from.
        """
        if name in self.__edges:
            edge = self.__edges.pop(name)
            self.degree(-1L*edge.multiplicity)

    def remove_parent_ref(self, wr):
        """
        Removes a weakref from the parent list.
        
        :param weakref.ref wr: The weakref to remove.
        """
        self.__parents.remove(wr)
        
    def remove_child_ref(self, wr):
        """
        Removes a weakref from the child list.
        
        :param weakref.ref wr: The weakref to remove.
        """
        self.__children.remove(wr)

    def parents(self):
        """
        Getter for the list of parent nodes.
        
        :rtype set(weakref.ref(graphism.node.Node)):
        """
        return self.__parents
    
    def children(self):
        """
        Getter for the list of child nodes.
        
        :rtype set(weakref.ref(graphism.node.Node)):
        """
        return self.__children

    def add_parent(self, parent_node, type_=None, weight_=1.0):
        """
        Adds a parent node to the set of parents. If the node already exists the 
        multiplicity of the node is increased. Also creates an edge from the parent to self.
        
        :param graphism.node.Node parent_node: The parent node to add.
        :param str type_: The type of edge to add.
        :param float weight_: The weight of the edge
        
        :rtype long: The multiplicity of the edge to parent_node.
        """
        node_name = parent_node.name()       
        edge = Edge(parent=weakref.ref(parent_node), 
                    child=weakref.ref(self),
                    type_=type_,
                    weight_=weight_)
                    
        return self.__edges[node_name].multiplicity
    
    def add_child(self, child_node, type_=None, weight_=1.0):
        """
        Adds a child node to the set of children. If the node already exists the
        multiplicity of the node is increased.
        
        :param graphism.node.Node child_node: The child node to add.
        :param str type_: The type of edge to add.
        :param float weight_: The weight of the edge
        
        :rtype long: The multiplicity of the edge to child_node.
        """
        node_name = child_node.name()
        edge = Edge(parent=weakref.ref(self),
                    child=weakref.ref(child_node),
                    type_=type_,
                    weight_=weight_)

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
    
    def infect(self, infection_function=None):
        """
        Gets or sets the propagation function on the node. This is analogous to infecting the node. 
        
        :param function infection_function: When passed it sets the function to infect other nodes.
        
        """
        if infection_function:
            self.__infection_function = infection_function
            infection_function(self)
        
        if self.__graph():
            self.__graph().remove_susceptible(self)
            self.__graph().add_infected(self)
        
        return self.__infection_function
        
    def recover(self, recovery_function=None):
        """
        Recover from infection.
        
        :param function recovery_function: The callback to execute during recovery
        """
        if random.random() < self.__recovery_probability(self):
            if recovery_function:
                self.__recovery_function = recovery_function
            else:
                self.__recovery_function(self)
            self.__recovery_function(self) 

            return True
        return False
                        
    def propagate_infection(self, l=None):
        """
        Propagates the lambda function (executes the function on) nodes 
        at random in the set of parents and children weighted by the 
        probability of transmission to the nodes in those sets.
        
        The lambda is executed on the node it propagates to.
        
        :param lambda l: The function to propagate. It must take the node as the first argument
        """
        if l:
            nodes = set([])
            for edge in self.edges().values():
                if edge.directed and self is edge.parent():
                    nodes.add(edge.child)
                else:
                    if self is not edge.child():
                        nodes.add(edge.child)
                    elif self is not edge.parent():
                        nodes.add(edge.parent)

            for n in nodes:
                if not self.__graph() or (self.__graph() and self.__graph().is_susceptible(n())):
                    probability = self.transmission_probability(n())
                    if random.random() < probability:
                        n().infect(l) # It transmits!
            
    def transmission_probability(self, to_node, probability_function=None):
        """
        Returns the probability of transmission from self to to_node.
        
        :param graphism.node.Node to_node: The node we're transmitting the lambda to
        :param lambda probability_function: An optional probability function. It will be passed from_node, to_node.
        
        :rtype float: A floating point number less than 1
        """
        if probability_function:
            return probability_function(self, to_node)
        elif self.__transmission_probability:
            return self.__transmission_probability(self, to_node)
        
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
