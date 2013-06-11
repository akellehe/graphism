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
    pass
