'''
Problem_1

1."Coefficient of variation" means the coefficient of 
the polynomial curve that fits the data best.
-False

2.If we let the k-means clustering algorithm run for a 
very long time, we will eventually end up with all the 
data points in one cluster.
-False

3.Training an algorithm on data set A and then testing 
it on a completely separate data set B is an example of 
unsupervised learning.
-False

4.Consider an undirected graph with non-negative weights 
that has an edge between each pair of nodes. The shortest 
distance between any two nodes is always the path that is 
the edge between the two nodes.
-False

5.A bimodal distribution is a probability distribution with 
two different modes. For example, exam grades can be bimodal 
when the students can be classified into one of two groups: 
either they understand the material or they understand less 
than half the material. A distribution made up of two normal 
distributions with equal standard deviations is noticeably 
bimodal if the means of each distribution are separated by 
at least 2 standard deviations.
The following line of python code will produce a bimodal 
distribution if called repeatedly:
random.gauss( 50,10) + random.gauss( 70, 10 )
-False

'''





'''
Problem_2

1.What does the following code print? Assume Pylab's estimation 
code is perfect - that is, if you calculate that it would print 
0.25, type 0.25 into the box rather than something like 0.24999999999. 
You may type in strings with or without quotes and separate the 
numbers by a space.
(CODE)
-0.0 2.0 4.0 8.0

2.Consider the following sets of measurements and answer the following 3 questions:
A. [0,1,2,3,4,5,6,7,8]
B. [5,10,10,10,15]
C. [0,1,2,4,6,8]
D. [6,7,11,12,13,15]
E. [9,0,0,3,3,3,6,6]
Select the two lists that have the same mean and variance.
-No two sets have the same mean and variance.

3.Consider following Python functions:
def possible_mean(L):
    return sum(L)/len(L)
def possible_variance(L):
    mu = possible_mean(L)
    temp = 0
    for e in L:
        temp += (e-mu)**2
    return temp / len(L)
Select the two lists that return the same values when passed 
into the possible_variance function that is defined above.
-B,D

4.Is the the answer to Problem 2-2 the same as the answer to 
Problem 2-3? If not, why are they different?
-They are different because of the 
way Python 2.7 handles division of integers. 

'''





'''
Problem_3A

'''
def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.
    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.
    The global variable CURRENTRABBITPOP is modified by this procedure.
    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    pRabbitRepr = 1.0 - CURRENTRABBITPOP / float(MAXRABBITPOP)
    for i in xrange(CURRENTRABBITPOP):
        if random.random() < pRabbitRepr:
            CURRENTRABBITPOP += 1
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.
    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.
    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).
    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.
    If it does not eat a rabbit, then with a 1/10 prob it dies.
    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP    
    
    pFoxEatRabbit = CURRENTRABBITPOP / float(MAXRABBITPOP)
    for i in xrange(CURRENTFOXPOP):
        if CURRENTRABBITPOP > 10 and random.random() < pFoxEatRabbit:
            CURRENTRABBITPOP -= 1
            if random.random() < 1/float(3):
                CURRENTFOXPOP += 1
        else:
            if CURRENTFOXPOP > 10 and random.random() < 9/float(10):
                CURRENTFOXPOP -= 1
            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.
    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.
    Both lists should be `numSteps` items long.
    """
    rPop = []
    fPop = []
    for i in xrange(numSteps):
        rabbitGrowth()
        foxGrowth()
        rPop.append(CURRENTRABBITPOP)
        fPop.append(CURRENTFOXPOP)        
    return (rPop, fPop)

'''
Problem_3B

2.At some point in time, there are more foxes than rabbits.
-True

3.The polyfit curve for the rabbit population is:
-A concave up curve (looks like a U shape)

4.The polyfit curve for the fox population is:
- A concave down curve (looks like a ∩ shape) 

5.Changing the initial conditions from 500 rabbits and 30 foxes 
to 50 rabbits and 300 foxes changes the general shapes of both 
the polyfit curves for the rabbit population and fox population.
-False

6.Let's say we make a change in the original simulation. That 
is, we are going to change one detail in the original simulation, 
but everything else will remain the same as it was explained 
in Problem 3 - Part A.
Now, if a fox fails in hunting, it has a 90 percent chance of 
dying (instead of a 10 percent chance, as in the original simulation).
Changing the probability of an unsuccessful fox dying from 
10% to 90% changes the general shapes of both the polyfit 
curves for the rabbit population and fox population.
-False

'''





'''
Problem_4A

1.
-SW

2.
-NA

3.
-SP

4.
-NA

5.
-NA

6.
-NA

7.
-BN

'''

'''
Problem_4B

8.
-SW

9.
-SP

10.
-BH

11.
-WW

'''






'''
Problem_5

In each code piece below, a graph is generated using the above 
node set by adding edges in some fashion. Your job is to examine 
the code and select the type of graph that will be generated. 
Your choices for each question will be: tree; graph (undirected graph); 
line graph; digraph (directed graph); complete graph or clique; 
bar graph; bipartite graph; loop or connected chain of nodes. 
Note that this last option refers to a graph that consists of 
one single, large loop or connected chain of nodes.

1.for i in range(len(nodes)):
    x = random.choice(nodes)
    y = random.choice(nodes)
    addEdge(x,y)
-digraph(directed graph)

2.for i in range(len(nodes)):
    x = random.choice(nodes)
    y = random.choice(nodes)
    addEdge(x,y)
    addEdge(y,x)
-graph(undirected graph)

3.for i in range(len(nodes)):
    w = random.choice(nodes)
    x = random.choice(nodes)
    y = random.choice(nodes)
    z = random.choice(nodes)
    addEdge(w,x)
    addEdge(x,y)
    addEdge(y,z)
    addEdge(z,w)
-digraph (directed graph)

4.for x in nodes:
    for y in nodes:
        addEdge(x,y)
        addEdge(y,x)
-complete graph or clique

5.The out degree of a node is the number of its neighbors, 
i.e. for a node x, its degree is the number edges, of the 
form (x, y_i), where y_i is some other node.
Which graph has the largest out degree per node?
-complete graph or clique

'''





'''
Problem_6

1.Suppose you are given a stack of documents and are told 
that documents with similar sets of keywords are about the 
same topic. Your job is to organize the documents as best 
you can by topic. The following 4 questions refer to this 
situation.

For this situation, it is best to use an unsupervised learning 
algorithm.
-True

2.Given the above information, which of the following would 
be the most appropriate feature to use?
-The number of times a particular 
 keyword appears in a document

3.Your boss comes back with a list of 60 specific keywords 
as well as 5 specific topics that each keyword is best associated 
with. Which of the following is true, given this additional 
information?
-We can use the k-means clustering 
 algorithm with k = 5 

4.Your boss comes back one last time with new information. 
He can now tell you the topic of each document. However, 
he found some more documents for which the topic is still 
unknown. Given this information, can we use a supervised 
learning algorithm to classify the new documents?
-Yes

5.Remember that in Problem Set 6, we used different linkage 
distance measures to calculate the distances between clusters 
and decide which cluster a point should belong to. Consider 
this new method of finding linkage distances, which makes use 
of the linkage distance methods from the problem set:
(CODE)
Answer the following 3 questions based on the above code.
-True

6.
- C0:a ||| C1:b,c,d,e,g ||| C2:f 

7.
-True

'''






'''
Problem_7

1.Assume we have built a graph G according to the above rules. 
Consider the lines of pseudocode:
z = random.choice(G.allNodes)
(x,y) = random.choice(G.allEdges)
add new edge z -> y
True or False? The node y is chosen with probability proportional 
to its popularity.
-True

2.To avoid selecting a self-edge (an edge from z to z), all edges 
pointing to z are first removed from allEdges before making 
the choice.
True or False? The following Python expression creates a list 
of all edges that does not include any edges into node z:
allEdgesExceptZ = []
for (x,y) in G.allEdges:
    if y != z:
        allEdgesExceptZ.append((x, y))
-True

3.The time to construct the list allEdgesExceptZ is O(E**2),
 where E is the number of edges.
-False

4.Consider the following procedure used to initialize a graph with n nodes:
def initializeGraph(n): # n is an integer, the number of nodes in the graph
    G = siteGraph() # Initializes an empty graph, with G.graphNodes set to []
    for i in range(n):
        G.graphNodes.append(newNode(i)) # newNode takes one parameter, the number of the node
    for i in range(n):
        x = G.graphNodes[i]
        y = G.graphNodes[ (i+1) % n ]
        x.addOutEdge(y)
    y.addInEdge(x)
    G.allEdges.append((x, y))
    return G.graphNodes
True or False? The procedure initializeGraph ensures that there is 
at least one path between any two nodes in the graph.
-True

5.Assume a random power-graph is created using the procedures 
explained above with 100 nodes. The following values are computed 
and plotted as a function of the number of edges, according to the 
following code:
maxDegrees, meanDegrees, meanDegreeVariances, meanShortestPaths = [],[],[],[]
graph = initializeGraph(n) 
for nEdges in range(n, n*n, n*n/10 ):
   graph.addEdges(nEdges)
   maxDegrees.append(graph.maxDegree())
   meanDegrees.append(graph.meanDegree())
   meanDegreeVariances.append(graph.meanDegreeVariances())
   meanShortestPaths.append(graph.meanShortestPath())
For each of the following plots, indicate which list was used to 
generate the plot:
-Mystery1 = meanDegrees
-Mystery2 = meanDegreeVariances
-Mystery3 = maxDegrees
-Mystery4 = meanShortestPaths
'''


