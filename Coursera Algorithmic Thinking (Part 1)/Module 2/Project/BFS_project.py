'''
commant regarding project
Raw Score   100.00 / 100.00
'''

import test_graphs as test
from collections import deque
import random
#import poc_queue

def bfs_visited(ugraph, start_node):
    '''
    Input:
    ugraph - undirected graph represented as adjacent list
    start_node - initial node. (in this case integer)

    Ounput:
    set of all visited by algorithm nodes represented as a set([])
    '''
    queue = deque()
    visited = set([start_node])
    queue.append(start_node)
    while len(queue) > 0:
        j_element = queue.popleft()
        for sosed in ugraph[j_element]:
            if sosed not in visited:
                visited.add(sosed)
                queue.append(sosed)
    return visited

def cc_visited(ugraph):
    '''
    Input:
    ugraph - undirected graph represented as adjacent list
    Output:
    list of sets of connected components of the graph
    '''
    rem_nodes = deque(node for node in ugraph)
    c_components = []
    while len(rem_nodes) != 0:
        node = random.choice(rem_nodes)
        visited = bfs_visited(ugraph, node)
        c_components.append(visited)
        for _ in visited:
            rem_nodes.remove(_)
    return c_components

def largest_cc_size(ugraph):
    '''
    Input:
    ugraph - undirected graph represented as adjacent list
    Output:
    integer represented the largest connected component
    '''
    sizes = cc_visited(ugraph)
    components_size = deque(len(comp) for comp in sizes)
    try:
        result = max(components_size)
    except ValueError:
        result = 0
    return result

def compute_resilience(ugraph, attack_order):
    '''
    Input:
    ugraph - undirected graph represented as adjacent list
    attack_order - list of nodes that will be attacked.
    Output:
    list of with the size of the largest connected components
    '''
    resilience = []
    for node in attack_order:
        if len(resilience) == 0:
            resilience.append(largest_cc_size(ugraph))
        ugraph.pop(node)
        for elem in ugraph:
            if node in ugraph[elem]:
                ugraph[elem].remove(node)
        resilience.append(largest_cc_size(ugraph))
    return resilience



print bfs_visited(test.GRAPH0, 0)
print cc_visited(test.GRAPH3)
print largest_cc_size(test.GRAPH7)
print compute_resilience(test.GRAPH2, [1, 3,5,7,2,4,6,8])