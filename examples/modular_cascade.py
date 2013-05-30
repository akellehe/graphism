import graphism.graph as gg
import graphism.graph_generators.barabasi_albert as ba
import graphism.graph_generators.uniform as ug


def cb_fun( node ):
  """ 
  a very simple callback function
  """
  return 0

edgelist = [(1,2),(1,3),(2,1),(3,1),(1,4),(4,1),(5,6),(6,5),(5,7),(7,5),(5,8),(8,5),(4,8)]
seed_graph = gg.Graph( edgelist )

m = 2
n = 500
g = ba.barabasi_albert( m, n, seed_graph)

# set the callback functions for the cascades
g.set_infection( cb_fun )
g.set_recovery( cb_fun )

# start the cascade with these nodes infected
g.infect_seeds( set([g.get_node_by_name(1), g.get_node_by_name(2), g.get_node_by_name(3) ]) )

# while there are still nodes that need to recover, allow the cascade to continue propagating.  print the results at each step (total infected) to stdout.
while( len( g.infected() ) != 0 ):
  g.propagate()
  print len( g.infected() )

