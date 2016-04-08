# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]
    
class WeightedEdge(Edge):
    def __init__(self, src, dest, weight1, weight2):
        self.src = src
        self.dest = dest
        self.weight1 = weight1
        self.weight2 = weight2
    def getTotalDistance(self):
        return self.weight1
    def getOutdoorDistance(self):
        return self.weight2
    def __str__(self):
        return '{0}->{1} {2}'.format(self.src, self.dest, (self.weight1, self.weight2))
    
class WeightedDigraph(Digraph):
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        total = edge.getTotalDistance()
        outdoor = edge.getOutdoorDistance()
        distances = (float(total),float(outdoor))
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest,distances])
    def childrenOf(self,node):
        #print node
        #print self.edges
        w = []
        for i in self.edges[node]:
            w.append(i[0])
        return w
    def __str__(self):
        res = ''
        for parent in self.edges:
            for children in self.edges[parent]:
                res = '{0}{1}->{2} {3}\n'.format(res, parent, children[0], children[1])
        return res[:-1]
   


nh = Node('h')
nj = Node('j')
nk = Node('k')
nm = Node('m')
ng = Node('g')
g = WeightedDigraph()
g.addNode(nh)
g.addNode(nj)
g.addNode(nk)
g.addNode(nm)
g.addNode(ng)
randomEdge = WeightedEdge(nk, nj, 53, 21)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nm, nk, 33, 28)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nm, nh, 48, 31)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nm, nk, 74, 56)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nm, nh, 35, 27)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nj, nm, 42, 42)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nm, nh, 47, 16)
g.addEdge(randomEdge)
randomEdge = WeightedEdge(nh, nj, 63, 25)
g.addEdge(randomEdge)
#print type(g.childrenOf(nh)[0])
g.childrenOf(nj)
g.childrenOf(nk)
g.childrenOf(nm)
g.childrenOf(ng)

