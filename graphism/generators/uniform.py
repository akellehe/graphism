import graphism.graph as gg

def trans_prob(a, b):
    """
    A simple transmission function, returning probability p = 0.9 for node a to infect node b
    
    :param graphism.node.Node a: the infected node
    :param graphism.node.Node b: the susceptible node
    
    :rtype float: A constant transmission probability of 90 percent
    """
    return 0.9

def build( n ):
    """
    Takes n, the number of nodes to be in the final graph, and returns a graph where each node is connected by one edge to every other node.  There are no self edges.  This is the graph assumed by the SIR model, so this graph can be used to simulate that model.
    
    :param int n: the number of nodes in the final graph
    
    :rtype graphism.graph.Graph: a uniform graph
    """
    edgelist = []
    nodelist = range(1,n+1)
    for i in nodelist:
        for j in nodelist:
            if i != j:
                edgelist.append((str(i),str(j)))
                
    return gg.Graph( edgelist, transmission_probability=trans_prob )
    
