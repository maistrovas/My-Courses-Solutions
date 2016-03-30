#import codeskulptor
#codeskulptor.set_timeout(20)
"""
Provided code for Application portion of Module 1
Imports physics citation graph
Answers 4/5
Application Grade is 12 out of 15
"""

# general imports
import random
import math
import matplotlib.pyplot as plt
import pylab
import urllib2
import DPATrial as alg_dpa_trial

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(900)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))
    return answer_graph
citation_graph = load_graph(CITATION_URL)

def make_complete_graph(num_nodes):
    '''
    takes a number of nodes and returnes 
    a dictionary  corresponding to a complete
    directed graph with the specified number of nodes
    - in iteration 'node' is a key, 'd[node]' is a value
    of a dictionary.
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
    comment
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
    comment
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
    comment
    '''
    total_nodes = float(len(digraph))
    distrib = in_degree_distribution(digraph)
    for node in distrib:
        distrib[node] = distrib[node] / total_nodes
    return distrib

'''
Question 1.
Citation_graph distribution (uncomment to load graph)
'''
distribution = norm_in_degree_distribution(citation_graph)

def extract_x_y(distribution):
    x = []
    y = []
    for i in distribution:
        x.append(i)
        y.append(distribution[i])
    return (x,y)

def plot (x,y, title):
    plt.figure('Application Plot')
    plt.title(title)
    plt.xlabel('Id-degree')
    plt.ylabel('Distribution')
    plt.loglog(x, y, 'bo')
    #plt.xlim(1, 1000)
    #plt.tight_layout()
    #plt.legend()
    plt.show()

'''
Question 2.
ER algoithm from Homework
'''
def algorithm_er(n, p):
    graph = {key: set() for key in xrange(n)}
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            if random.random() < p:
                graph[i].add(j)
            if random.random() < p:
                graph[j].add(i)
    return graph

er_graph = algorithm_er(2000, 0.5)
er_distribution = norm_in_degree_distribution(er_graph)


#plot(extract_x_y(er_distribution)[0],extract_x_y(er_distribution)[1],
#    'ER graph in-degree distribution')

'''
Question 3.
DPA Algorithm
Answer:
n = 27600
m = 13
'''
def avg_out_degree(graph):
    N = float(len(graph))
    return sum(len(x) for x in graph.itervalues()) / N

def algorithm_dpa(n, m):
    graph = make_complete_graph(m)
    dpa = alg_dpa_trial.DPATrial(m)
    for i in xrange(m, n):
        graph[i] = dpa.run_trial(m)
    return graph


print('avg_out_degree', avg_out_degree(citation_graph))
dpa = algorithm_dpa(27700, 13)
norm_dist = norm_in_degree_distribution(dpa)

plot(extract_x_y(norm_dist)[0],extract_x_y(norm_dist)[1],
    'PDA-genereted graph, in-degree distribution')




