
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import operator as op
import copy

# these algorithms should all work on networkx graphs
# err, both digraphs and graphs?


# TODO: LABEL AXES
# TODO: verify in_degree vs. out_degree makes sense for both hist and ccdf
# TODO: for digraph, when getting CL and CL-avg, treat as undirected

def degree_hist(g, title, xaxis, yaxis, out=True):
    # TODO: for authors, shouldn't it be degree+1?
    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    if out:
        ax.hist([g.degree(n) for n in g], bins=30, log=True)
        #ax.hist(np.log([g.degree(n) for n in g]), bins=30)
    else: # in-degree
        ax.hist([g.in_degree(n) for n in g], bins=30, log=True)
        #ax.hist(np.log([g.in_degree(n) for n in g]), bins=30)
    plt.show()

def degree_ccdf(g, title, xaxis, yaxis, out=True):
    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    degrees = []
    if out:
        degrees = np.array([float(g.degree(n)) for n in g])
    else: # in-degree
        degrees = np.array([float(g.in_degree(n)) for n in g])
    max_degree = np.max(degrees)
    degrees /= sum(degrees) # normalize
    ccdf = 1-np.cumsum(degrees)
    x = np.arange(0,max_degree,max_degree/len(ccdf))
    #print len(x)
    #print len(ccdf)
    ax.plot(x, ccdf[:len(x)])
    plt.show()

""" fns for counting triangles and triples from set1 """
def nCr(n, r):
    # n choose r, from http://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

def count_triples(i, g):
    """ Count triples in g centered on i. """
    num_neighbors = len(g[i].keys())
    if num_neighbors < 2: return 0 # should probably modify nCr to do this...
    return nCr(num_neighbors, 2)
def count_triangles(i, g):
    """ Count trianges in g centered on i. """
    neighbors = set(g[i].keys())
    checked = set()
    triangles = 0
    # find connections between neighbors
    for n1 in neighbors:
        for n2 in neighbors - checked:
            if n1 in g[n2]:
                triangles += 1
        checked |= {n1} # avoid double-counting
    return triangles

def count_total_triples(g):
    # count total number of triples in graph g
    return sum([count_triples(i,g) for i in g.nodes()])
def count_total_triangles(g):
    # count total number of triangles in graph g
    g2 = g.copy()
    triangles = 0
    while g2.nodes():
        i = g2.nodes()[0]
        triangles += count_triangles(i,g2)
        g2.remove_node(i)
    return triangles

def Cl(g):
    return 3.*count_total_triangles(g) / count_total_triples(g)

def Cl_i(i, g):
    triples = count_triples(i,g)
    if triples == 0: return 0
    return float(count_triangles(i,g)) / triples
def Cl_avg(g):
    cl_sum = 0
    for i in g.nodes():
        cl_sum += Cl_i(i,g)
    return float(cl_sum) / len(g.nodes())


""" DIAMETER THINGS """
def fw_dist(g):
    # do floyd-warshall on g, return distance matrix M s.t. M[a,b] is
    # distance from a to b
    # NOTE: In this code, the line: np.minimum(dist, dist[k,:] + dist[:,k])
    #       in the floyd-warshall loop was taken from NetworkX source code.
    #       Prof. Wierman gave permission for this on piazza, so hopefully ok.

    # initialize everything to infinity and initialize self-links on diagonal
    dist = np.matrix(np.ones((len(g), len(g)))*np.inf)
    np.fill_diagonal(dist,0)
    # init immediate adjacencies
    for n1 in g:
        for n2 in g[n1]:
            dist[n1,n2] = 1.
    # do floyd-warshall WITH VECTORIZATION FROM NETWORKX
    for k in range(len(g)):
        #print k,' / ',len(g)
        dist = np.minimum(dist, dist[k,:] + dist[:,k])
    # return final matrix
    return dist


def max_diameter(g, data=None):
    if data != None: return np.amax(data)
    return np.amax(fw_dist(g))
def avg_diameter(g, data=None):
    # TODO: uhh, should exclude infinite things!?!?!?!?
    # assumes data is fw_dist(g)
    if data != None: return data.sum() / (len(g)**2)
    return fw_dist(g).sum() / (len(g)**2)


def highest_pagerank_node(g_init, explored, iterations=10):
    # get the highest pagerank node in g (well, at least I think this is 
    # pagerank...)
    # implemented using pseudocode from:
    # http://www.ccs.northeastern.edu/home/daikeshi/notes/PageRank.pdf
    # TODO: need to specify number iterations??

    g = nx.DiGraph(g_init)

    opg = dict() # initial pagerank dict
    npg = dict() # new_step pagerank dict
    d = 0.85   # damping factor
    N = float(len(g)) # number of pages

    # initialize pagerank dict
    for p in g:
        opg[p] = 1./N

    # iterate algorithm
    for i in range(iterations):
        dp = 0 
        
        # get pagerank from pages without outlinks
        for p in [n for n in g.nodes() if g.degree(n)==0]:
            dp += d*opg[p]/N

        # get pagerank from random jump
        for p in g:
            npg[p] = dp + (1.-d)/N
            # get pagerank from in-links
            for ip in g.predecessors(p):
                npg[p] += d*opg[ip]/float(len(g.successors(ip)))
        
        #update pagerank
        opg = copy.deepcopy(npg) # hmm...
        npg = dict() # not sure necessary

    # remove explored nodes...sorta ugly
    for n in explored: del opg[n]
    # return node with highest pagerank that isn't in explored
    best_index = None
    try:
        best_index = max(opg.iterkeys(), key=(lambda k: opg[k]))
    except Exception,e:
        print "no max arg found"
        return None
    return best_index
