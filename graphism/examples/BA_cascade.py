import graphism.graph as gg
import graphism.graphs.barabasi_albert as ba
import graphism.graphs.uniform_graph as ug

def cb_fun( node ):
  return 0

m = 2   # edges to add at each step
N = 50  # total number of nodes

seed_graph = ug.build_uniform_graph( 10 )
g = ba.barabasi_albert( m, N, seed_graph )
g.set_infection( cb_fun )
g.set_recovery( cb_fun )

g.infect_seeds( set([g.get_node_by_name('1'), g.get_node_by_name('2'), g.get_node_by_name('3') ]) )
while( len( g.infected() ) != 0 ):
  g.propagate()
  print len( g.infected() )
