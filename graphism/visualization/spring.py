import random
import math
import numpy

from matplotlib import pyplot as plt 


MAX_ITERATIONS = 1000000
DT = 0.01
EPSILON = 1e-6
WEAK_FORCE_MULTIPLIER = 1
K_CONSTANT = 1
FRICTION_COEFFICIENT = 10000.0

"""
 INITIALIZATION
 Set 2-d position at random for each node.
 Set spring constant as a function of the weight and multiplicity of edges.
 Set charge as a function of the degree of a node
"""
def initialize_positions(graph, domain=100, yrange=100):
    """
    Initializes the positions of each node in the graph at random.
    
    :param graphism.graph.Graph graph: The graph to initialize the positions of the nodes for.
    :param int domain: The maximum x-position allowed for the visualization.
    :param int yrange: The maximum y-position allowed for the visualization.
    
    """
    x_values = range(domain)
    y_values = range(yrange)
    for node in graph.nodes():
        node.position = [ random.random(), random.random() ]
        node.velocity = [0.0,0.0]
        node.forces = [0.0,0.0]
        for edge in node.edges().values():
            if not hasattr(edge, 'k'):
                edge.k = edge.weight_ * edge.multiplicity
"""        
 EQUILIBRATION
 Calculate direction and magnitude of force at each node.
 Sum the forces at each node
 Move one dx, dy based on that force for each node
"""
def calculate_forces(graph):
    """
    Calculates forces of each node on each other in the graph. Sums them to a vector.
    
    :param graphism.graph.Graph graph: The graph to calculate the forces on
    
    """
    a_nodes = set(graph.nodes())
    b_nodes = set(graph.nodes())
    
    for a in a_nodes:
        a.forces = [0.0, 0.0]
    
    for a in a_nodes:
        for b in b_nodes:
            if a == b:
                continue
            
            F_k_s = 0
            F_k_w = 0
            
            # Distance from a to b
            r = math.sqrt((b.position[0] - a.position[0]) ** 2.0 + (b.position[1] - a.position[1]) ** 2.0)
            if a.name() == 1 and b.name() == 2:
                print "Distance from 1 to 2: %s" % r
            
            v = math.sqrt((a.velocity[0] ** 2.0) + (a.velocity[1] ** 2.0))
            
            if r == 0:
                r = 1e-9
            
            # Magnitude of force due to compactness (outward)
            print "Velocity :%s" % v
            F_k_w = - (K_CONSTANT * r) + (FRICTION_COEFFICIENT * v)

            # Magnitude of force due to connectedness (inward)
            #if a.is_parent_of(b) or b.is_parent_of(a):
            #    F_k_s = ( a[b.name()].k if b.name() in a else b[a.name()].k ) * r * STRONG_FORCE_MULTIPLIER

            # Direction of force from a to b:
            x = ( b.position[0] - a.position[0] ) / (r ** 2.0)
            y = ( b.position[1] - a.position[1] ) / (r ** 2.0)

            if F_k_w != 0:
                a.forces[0] += (F_k_w * x)
                a.forces[1] += (F_k_w * y)

            if F_k_s != 0:
                a.forces[0] += (F_k_s * x)
                a.forces[1] += (F_k_s * y)

def apply_forces(graph):
    """
    Uses the previously set velocity to increment position. Expects forces to be set on every node in the graph. Applies that force over one dt to increment the velocity. 
    
    :param graphism.graph.Graph graph: The graph to iterate over applying forces to nodes
    
    :rtype float: The total kinetic energy of the graph
    """
    K = 0
    for node in graph:            
        node.velocity[0] += node.forces[0] * DT
        node.velocity[1] += node.forces[1] * DT
        
        K += ((node.velocity[0] ** 2.0) + (node.velocity[1] ** 2.0))
        
        node.position[0] += node.velocity[0] * DT
        node.position[1] += node.velocity[1] * DT

    return K

"""
 FINALIZATION
 Calculate the overall energy of the system 
 Stop iterating when the energy of the system is within some epsilon value
"""
def layout(graph):
    initialize_positions(graph)
    K = numpy.inf
    K_t = []
    dK = None
    for i in range(MAX_ITERATIONS):
        calculate_forces(graph)
        K = apply_forces(graph)
        K_t.append(K)
        if K_t:
            dK = K - K_t[-1]
        if dK and dK < EPSILON:
            break
    plt.plot(K_t)
    plt.show()
    
    