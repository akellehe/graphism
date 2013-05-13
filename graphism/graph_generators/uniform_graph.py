import graphism.graph as gg

def trans_prob(a, b):
  """
  a simple transmission function, returning probability p = 0.5 for node a to infcet node b

  Required parameters:
  :param graphism.Node a: the infected node
  :param graphism.Node b: the susceptible node
  """

  return 0.5

def build( n ):
  """
  Takes n, the number of nodes to be in the final graph, and returns a graph where each node is connected by one edge to every other node.  There are no self edges.  This is the graph assumed by the SIR model, so this graph can be used to simulate that model.

  Required parameters:
  :param int n: the number of nodes in the final graph
  """
  n = n + 1
  edgelist = []
  nodelist = range( n )
  nodelist.remove( 0 )
  for i in nodelist:
    for j in nodelist:
      if i != j:
        edgelist.append((str(i),str(j) ))
  
  g = gg.Graph( edgelist, transmission_probability=trans_prob )
  return g

