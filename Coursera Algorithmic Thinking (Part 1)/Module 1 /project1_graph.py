'''
Project 1 - Degree distributions for graphs
Raw Score   100.00 / 100.00
'''

import test_graphs as test

EX_GRAPH0 = {0:set([1,2]),1:set([]),2:set([])}
EX_GRAPH1 = {0:set([1,4,5]), 1:set([2,6]),
             2:set([3]), 3:set([0]), 4:set([1]), 5:set([2]), 6:set([]) }
EX_GRAPH2 = {0:set([1,4,5]), 1:set([2,6]), 2:set([3,7]),3:set([7]),
             4:set([1]), 5:set([2]), 6:set([]), 7:set([3]), 8:set([1,2]), 9:set([0,3,4,5,6,7])}


def make_complete_graph(num_nodes):
    '''
    takes a number of nodes and returnes 
    a dictionary  corresponding to a complete
    directed graph with the specified number of nodes
    - in iteration 'node' is a key, 'd[node]' is a value
    of a dictionary.

    num_nodes - int.
    '''
    complete_graph = {}
    assert type(num_nodes) is int, "Input is not appropriate!"
    if num_nodes == 0:
        return set([0])
    elif num_nodes == 1:
        return {0:set([])}
    else:
        for node in range(num_nodes):
            complete_graph[node] = set()
            for neightbor in range(num_nodes):
                if neightbor != node:
                    complete_graph[node].add(neightbor)
                else:
                    continue
        return complete_graph
def compute_in_degrees(digraph):
    '''
    computes the in-degrees for the nodes in
    the graph. The function should return a 
    dictionary with the same set of keys 
    (nodes) as digraph whose corresponding 
    values are the number of edges whose head 
    matches a particular node.

    digraph - Directed graph, repr. as dictionary
    '''
    in_degrees = {}
    for node in digraph:
        counter = 0
        for neightbor in digraph:
            if node in digraph[neightbor]:
                counter +=1
            in_degrees[node] = counter
            
    return in_degrees

def in_degree_distribution(digraph):
    '''
    Computes the unnormalized distribution of the
    in-degrees of the graph. The function should
    return a dictionary whose keys correspond
    to in-degrees of nodes in the graph. The
    value associated with each particular i
    n-degree is the number of nodes with that 
    in-degree. In-degrees with no corresponding 
    nodes in the graph are not included in the dictionary.

    digraph - Directed graph, repr. as dictionary
    '''
    digraph = compute_in_degrees(digraph)
    distrib = {}
    for node in digraph:
        counter = 0
        for indegree in digraph:
            if digraph[node] == digraph[indegree]:
                counter +=1
        distrib[digraph[node]] = counter
    return distrib


def norm_in_degree_distribution(digraph):
    '''
    Normalizes in_degree_distribution
    '''
    total_nodes = float(len(digraph))
    distrib = in_degree_distribution(digraph)
    for node in distrib:
        distrib[node] = distrib[node] / total_nodes
    return distrib
#print in_degree_distribution(test.GRAPH2)
#print norm_in_degree_distribution(test.GRAPH2)
