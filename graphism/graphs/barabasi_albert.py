import graphism as g
import random as r
import graphism.graph as gg
import graphism.node as gn
def barabasi_albert( m, N, seed_graph=None ):
  if N < 2:
    print "graph needs more nodes"
  if seed_graph == None:
    node_name = 3
    BA = gg.Graph([ ('1','2') ])
  else:
    node_name = len( seed_graph.nodes() ) + 1
    BA = seed_graph
  while len( BA.nodes() ) < N:
#    for node in BA.nodes():
#      print node.name(), node.degree()
    new_edges_to = choose_nodes( BA, m )
    new_node = gn.Node( name=str(node_name) )
    node_name += 1

    BA.add_node( new_node )
    for edge_to in new_edges_to:
      BA.add_edge_by_node_sequence( new_node.name() , edge_to )
  return BA
    
    
def choose_nodes( g, m ):
  tot_deg = 0
  for node in g.nodes():
    tot_deg += node.degree()
  probs = [ (node.name(), float( node.degree()) / float( tot_deg) )  for node in g.nodes() ]
  cdf = [ 0 ]
  for i, dat in enumerate( probs ):
    name = dat[ 0 ]
    p_i = dat[ 1 ] 
    cdf.append( cdf[ i ] + p_i )
  # choose m nodes
  nodelist = []
  while len(nodelist) < m:
    n = r.random()
    for i, entry in enumerate( cdf ):
      if n > entry and n < cdf[ i + 1]:
        res = probs[i][0]
        if res not in nodelist:
          nodelist.append( res )
          break
        else:
          continue
  return nodelist

# gr = barabasi_albert( 2, 10 )
