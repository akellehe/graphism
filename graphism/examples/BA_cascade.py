import graphism.graph as gg
import graphism.graph_generators.barabasi_albert as ba
import graphism.graph_generators.uniform_graph as ug

def cb_fun( node ):
  """ 
  a very simple callback function
  """
  return 0

# set the parameters for the BA graph generator
m = 2   # edges to add at each step
N = 50  # total number of nodes

# just for fun, build the BA graph from a uniform seed graph
seed_graph = ug.build( 10 )
g = ba.barabasi_albert( m, N, seed_graph )

# set the callback functions for the cascades
g.set_infection( cb_fun )
g.set_recovery( cb_fun )

# start the cascade with these nodes infected
g.infect_seeds( set([g.get_node_by_name('1'), g.get_node_by_name('2'), g.get_node_by_name('3') ]) )

# while there are still nodes that need to recover, allow the cascade to continue propagating.  print the results at each step (total infected) to stdout.
while( len( g.infected() ) != 0 ):
  g.propagate()
  print len( g.infected() )
