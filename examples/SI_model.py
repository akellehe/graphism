import graphism.graph as gg
import graphism.graph_generators.uniform as ug

"""
  This is an example of how to simulate an SIR model using the 
  graph_generators.uniform_graph module along with the cascade functionality of 
  the graphism.Graph object.  The output, to stdout, is the I curve.  The time
  units are arbitrary, and this model is technically a discretized version of
  the SIR model.
"""

def cb_fun( node ):
  """
  super simple callback function
  """
  return 0

# set the parameters for the uniform graph
N = 300

# build the graph
g = ug.build( N )

#set the callback function for the cascade
g.set_infection( cb_fun )

# choose some nodes to start out infected
g.infect_seeds( set([g.get_node_by_name('1'), g.get_node_by_name('2'),g.get_node_by_name('3'),g.get_node_by_name('4')]) )

# while there are still infected nodes, propagate the cascade.  print the volume infected at each step to stdout
while( len(g.infected() ) > 0 ):
  g.propagate()
  print len( g.infected() )
