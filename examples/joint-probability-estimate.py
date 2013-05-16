#!/usr/bin/env python

from graphism import graph as gg

ITERATIONS = 100000

g = gg.Graph(length=lambda e: 1 - e.weight_)
tp = lambda a, b: a[b.name()].weight_
edges = [{
          "parent": 1,
          "child": 2,
          "directed": True,
          "transmission_probability": tp,
          "weight_": 0.5          
         },{
          "parent": 1,
          "child": 3,
          "directed": True,
          "transmission_probability": tp,
          "weight_": 0.2,
         },{
           "parent": 2,
           "child": 3,
           "directed": True,
           "transmission_probability": tp,
           "weight_": 0.3 
         },{
           "parent": 3,
           "child": 5,
           "directed": True,
           "transmission_probability": tp,
           "weight_": 0.1               
         }]

infections = 0
for i in range(ITERATIONS):

    for e in edges:
         g.add_edge_by_node_sequence(**e)

    g.infect_seeds([g[1]])

    for t in range(4):
      g.propagate()

    infected = g[1] in g.infected()

    if infected:
      infections += 1

print "INFECTED %s percent of the time" % (float(infections) / float(ITERATIONS))



