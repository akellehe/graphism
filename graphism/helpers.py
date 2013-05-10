def tp(from_node, to_node):
    edge = from_node.edges()[to_node.name()]
    multiplicity = edge.multiplicity
    degree = from_node.degree()
    if degree == 0L:
        return 0.0
    else:
        return float(multiplicity) / float(degree)

def rp(n):
    return 0.5

def return_none():
    return None

def return_none_from_one(n):
    return None

