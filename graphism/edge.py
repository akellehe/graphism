import weakref

class Edge(object):
    """
    Represents a Edge between the node containing the Edge and a parent or child node.
    
    :param weakref(graphism.node.Node) parent: A weak reference to the parent node. 
    :param weakref(graphism.node.Node) child: A weak reference to the child node.
    :param long multiplicity: The multiplicity of the edge.
    :param str type_: The type of edge
    :param float weight_: The weight of the edge.
    :param bool directed: Whether or not the edge is directed.
    :param function length: A function returning the length of the edge. Takes the edge as the only argument.
    """    
    node = None
    multiplicity = None
    type_ = None
    directed = None
    weight_ = None
    child = None
    parent = None
    
    def __init__(self, parent, child, multiplicity=1L, type_=None, weight_=1.0, directed=False, length=None):
        assert isinstance(parent, weakref.ref)
        assert isinstance(child, weakref.ref)
        
        self.parent = parent                   
        self.child = child
        self.multiplicity = multiplicity
        self.type_ = type_
        self.weight_ = weight_
        self.directed = directed
        
        self.__length = length or (lambda e: e.weight_)
        
        self.__parent_name = parent().name()
        self.__child_name = child().name()
        
        def parent_cleanup(wr):
            self.parent().remove_child_ref(wr) 
            self.parent().remove_all_edges_by_name(self.__child_name)
        
        def child_cleanup(wr):
            self.child().remove_parent_ref(wr)
            self.child().remove_all_edges_by_name(self.__parent_name)
            
        child().parents().add(weakref.ref(parent(), child_cleanup))
        parent().children().add(weakref.ref(child(), parent_cleanup))
        
        parent().add_edge(child().name(), self)
        child().add_edge(parent().name(), self)
        
    def to_dict(self):
        """
        Converts the graphism.edge.Edge to a dictionary representation of itself with the graphism.node.Node objects represented as a unicode of their name.
        
        :rtype dict: A dictionary representation of the edge.
        """
        return {
                'from_': self.parent().name(),
                'to_': self.child().name(),
                'weight_': self.weight_,
                'directed': self.directed,
                'type_': self.type_,
                'multiplicity': self.multiplicity,
                'length': self.__length
                }

    def length(self):
        return self.__length(self)

    def edge_to_tuple(self):
        """
        Returns a tuple containing the names of a given edge's parent and child nodes.

        :rtype tuple: A two-item tuple containing the names of the edge's parent and child nodes.
        """
        return (self.parent.name(), self.child.name())
