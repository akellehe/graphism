import weakref

class Edge(object):

    parent = None
    child = None
    multiplicity = 1L
    weight = 1.0
    graph = None

    def __init__(self, parent, child, multiplicity=1L, weight=1.0, graph=None):
        """
        Represents a Edge between the node containing the Edge and a parent or child node.
        
        :param str parent: The unique name of the parent node
        :param str child: THe unique name of the child node.
        :param long multiplicity: The multiplicity of the edge.
        :param float weight: The weight of the edge.
        """    
        self.parent = parent
        self.child = child
        self.multiplicity = multiplicity
        self.weight = weight
        self.graph = graph
                
    def __str__(self):
        return "<%s -> %s>" % (self.parent, self.child)