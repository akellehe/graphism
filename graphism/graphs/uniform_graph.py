import graphism.graph as gg


def trans_prob(a, b):
  return 0.5

def build_uniform_graph( N ):
  N = N + 1
  edgelist = []
  nodelist = range( N )
  nodelist.remove( 0 )
  for i in nodelist:
    for j in nodelist:
      if i != j:
        edgelist.append((str(i),str(j) ))
  
  g = gg.Graph( edgelist, transmission_probability=trans_prob )
  return g

