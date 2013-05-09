import graphism.graph as gg
import graphism.graphs.uniform_graph as ug

def cb_fun( node ):
  return 0

N = 50
g = ug.build_uniform_graph( N )
g.set_infection( cb_fun )

g.infect_seeds( set([g.get_node_by_name('1')]) )
while( len(g.infected() ) < N ):
  g.propagate()
  print len( g.infected() )
