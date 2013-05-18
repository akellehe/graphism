#!/usr/bin/env python
"""
This script tests the SIR behavior of a graph. Adjust the parameters below
to play around. At the end a line graph of the ensemble of iterations will 
be plotted.

"""
import sys
import numpy
try:
    from matplotlib import pyplot as plt 
except:
    print "Sorry, matplotlib==1.2.1 is required to run this example."
    sys.exit(1)

from graphism import graph as g

NODES = 100

PERIOD = 24
infection_curves = []
SEEDS = 5 # nodes initially infected
TRANSMISSION_PROBABILITY = 0.01 # *100 = percent
RECOVERY_PROBABILITY = 0.002 # *100 = percent
ITERATIONS = 10

if __name__ == '__main__':
    
    tp = lambda parent, child: TRANSMISSION_PROBABILITY
    rp = lambda node: RECOVERY_PROBABILITY
    
    for iteration in range(ITERATIONS):
        infected = []
        edges = []
        seed_nodes = []
        
        for i in range(NODES):
            for j in range(NODES):
                if i != j:
                    edges.append((i,j))
        
        graph = g.Graph(edges,
                        transmission_probability=tp,
                        recovery_probability=rp)    
        
        graph.infect_seeds([graph.get_node_by_name(n) for n in range(SEEDS)])
        
        for t in range(PERIOD):
            graph.propagate()
            infected.append(len(graph.infected()))
            
        infection_curves.append(infected)
        
        sys.stderr.write('.')
        sys.stderr.flush()
    
    plt.plot([numpy.mean(tup) for tup in zip(*infection_curves)])
    plt.show()

print [int(numpy.mean(tup)) for tup in zip(*infection_curves)]