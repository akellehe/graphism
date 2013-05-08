import weakref

class Edge(object):
    """
    Represents a Edge between the node containing the Edge and a parent or child node.
    
    """
    node = None
    multiplicity = None
    type_ = None
    directed = None
    weight_ = None
    child = None
    parent = None
    
    def __init__(self, parent, child, multiplicity=1L, type_=None, weight_=1.0, directed=False):
        """
        Initializer for the Edge. 
        
        :param weakref(graphism.node.Node) parent: A weak reference to the parent node. 
        :param weakref(graphism.node.Node) child: A weak reference to the child node.
        :param long multiplicity: The multiplicity of the edge.
        :param str type_: The type of edge
        :param float weight_: The weight of the edge.
        :param bool directed: Whether or not the edge is directed.
        """    
        assert isinstance(parent, weakref.ref)
        assert isinstance(child, weakref.ref)
        
        self.parent = parent                   
        self.child = child
        self.multiplicity = multiplicity
        self.type_ = type_
        self.weight_ = weight_
        self.directed = directed
        
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

