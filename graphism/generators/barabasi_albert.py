import random as r

import graphism as g
import graphism.graph as gg
import graphism.node as gn

def barabasi_albert( m, n, seed_graph=None ):
  """
  The Barabasi-Albert model is a preferential attachment model that
  dynamically generates an undirected, unweighted  graph with small 
  world structure (geodesic length grows ~ ln(n)/ln(ln(n)) ), and 
  clustering around central nodes.  The specified seed_graph will 
  cause the graph generated to prefer to keep building on the modular 
  structure that is already present.  
  
  :param int m: the number of edges directed from each newly added node
  :param int n: the total number of nodes the final graph should contain
  :param graphism.graph.Graph seed_graph: the graph on which to build the final graph.  default is two nodes with one edge connecting them.

  """

  if n < 2:
    print "graph needs more nodes"
  if seed_graph == None:
    node_name = 3
    BA_graph = gg.Graph([ ('1','2') ])
  else:
    node_name = len( seed_graph.nodes() ) + 1
    BA_graph = seed_graph
  while len( BA_graph.nodes() ) < n:
    new_edges_to = choose_nodes( BA_graph, m )
    new_node = gn.Node( name=str(node_name) )
    node_name += 1

    BA_graph.add_node( new_node )
    for edge_to in new_edges_to:
      BA_graph.add_edge_by_node_sequence( new_node.name() , edge_to )
  return BA_graph
        
def choose_nodes( g, m ):
  """
  choose m nodes from the graph g, where the nodes are chosen with probabilities proportional to their total degree.

  :param graphism.graph.Graph g: the graph from which to choose the nodes
  :param int m: the number of nodes to choose
  :rtype list(graphism.node.Node): list of chosen nodes
  """
  tot_deg = 0
  for node in g.nodes():
    tot_deg += node.degree()
  probs = [ (node.name(), float( node.degree()) / float( tot_deg) )  for node in g.nodes() ] # calculate node selection probabilities based on degree
  cdf = [ 0 ] # cumulative distribution function of node probability list, to be calculated
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

