"""
Provided code for Application portion of Module 2

Answers 4/6
Application Grade is 13 out of 15

Text Answers
-Question 2:
All three graphs are resilient in this case.

Question5:
-UPA and ER graphs are steel resilient
 (UPA is very close to overcoming 25% roughnes)
  in this type of attack.
"""

# general imports
import urllib2
import random
import timeit
import time
import math
import UPA
from collections import deque
from random import shuffle
import BFS_project as project
import matplotlib.pyplot as plt
import numpy as np
# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    counter = 0
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            counter +=1
            answer_graph[node].add(int(neighbor))
    print 'Number network edges = ', counter / 2
    return answer_graph

def er_graph(n, p):
    '''
    implementation of ER algorithm

    n - final number of nodes
    p - probability
    '''
    graph = {key: set() for key in xrange(n)}
    counter = 0
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            if random.random() < p:
                counter += 1
                graph[i].add(j)
                graph[j].add(i)
    print 'Number of ER-edges=', counter
    return graph

##UPA-Algorithm
def algorithm_upa(n, m):
    '''
    implementation of UPA algorithm
    n - final number of nodes
    m - number of existing nodes
    p - probability for er_graph
    '''
    graph = er_graph(m, 1)
    upa = UPA.UPATrial(m)
    counter = 0
    for i in xrange(m, n):
        new_edges = upa.run_trial(m)
        graph[i] = new_edges
        for node in new_edges:
            graph[node].add(i)
    return graph

def random_order(graph):
    '''
    takes a graph and returns a list
    of the nodes in the graph in some random order
    '''
    result = deque()
    for node in graph:
        result.append(node)
    shuffle(result)
    return result

loaded_graph = load_graph(NETWORK_URL)
er_ggraph = er_graph(1239, 0.004)  
upa_graph = algorithm_upa(1239, 3)


def count_Uedges(ugraph):
    '''
    count edges in the graph
    '''
    counter = 0
    for i in ugraph:
        for j in ugraph[i]:
            counter +=1
    return counter/2

# print 'UPA edges = ', count_Uedges(upa_graph)
# print 'ER edges =', count_Uedges(er_ggraph)
# print 'Network graph edges =', count_Uedges(loaded_graph)

def plotting(net_g, er_g, upa_g, question):
    """
    Plot an example with two curves with legends
    x -  number of nodes removed
    y - size of the largest connect component
    in the graphs resulting from the node removal.
    """
    if question == 1:
        print 'The function plots question 1'
        network_order = random_order(net_g)
        er_order = random_order(er_g)
        upa_order = random_order(upa_g)
    if question == 4:
        print 'The function plots question 4'
        network_order = targeted_order(net_g)
        er_order = targeted_order(er_g)
        upa_order = targeted_order(upa_g)

    network_resil = project.compute_resilience(net_g, network_order)
    er_resil = project.compute_resilience(er_g, er_order)
    upa_resil =  project.compute_resilience(upa_g, upa_order)

    xvals_net = np.array([node for node in range(len(network_order) +1 )])
    xvals_er = np.array([node for node in range(len(er_order) +1 )])
    xvals_upa = np.array([node for node in range(len(upa_order) +1 )])

    yvals_net = np.array(network_resil) 
    yvals_er = np.array(er_resil)
    yvals_upa = np.array(upa_resil)

    plt.figure('Application2 Plot')
    plt.title('Resilience comparison')
    plt.xlabel('Removed nodes')
    plt.ylabel('Largest conected component')
    plt.plot(xvals_net, yvals_net, '-b', label='Network-Data')
    plt.plot(xvals_er, yvals_er, '-r', label='ER-Algorithm (p = 0.004)')
    plt.plot(xvals_upa, yvals_upa, '-g', label='UPA-Algorithm (m = 3)')
    plt.legend(loc='upper right')
    plt.show()
'''
Questions 1,4
'''
plotting(loaded_graph, er_ggraph, upa_graph, 1)
#plotting(loaded_graph, er_ggraph, upa_graph, 4)

def measure_targeted_order(n, m, func):
    graph = algorithm_upa(n, m)
    return timeit.timeit(lambda: func(graph), number=1)

def fast_targeted_order(ugraph):
    '''
    comment
    '''
    ugraph = copy_graph(ugraph)
    N = len(ugraph)
    degree_sets = [set()] * N
    for node, neighbors in ugraph.iteritems():
        degree = len(neighbors)
        degree_sets[degree].add(node)
    order = []
    for k in range(N - 1, -1, -1):
        while degree_sets[k]:
            u = degree_sets[k].pop()
            for neighbor in ugraph[u]:
                d = len(ugraph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)
            order.append(u)
            delete_node(ugraph, u)
    return order

def question3():
    '''
    Function plotting Question 3
    '''
    xs = range(10, 1000, 10)
    m = 5
    ys_tagreted = [measure_targeted_order(n, m, targeted_order) for n in xs]
    ys_fast_targeted = [measure_targeted_order(n, m, fast_targeted_order) for n in xs]
    plt.plot(xs, ys_tagreted, '-r', label='targeted_order')
    plt.plot(xs, ys_fast_targeted, '-b', label='fast_targeted_order')
    plt.title('Targeted order functions performance (desktop Python)')
    plt.xlabel('Number of nodes in the graph')
    plt.ylabel('Execution time')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
'''
Question3
Include only plotting
'''
question3()








