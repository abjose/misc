import fileinput
import sys
import networkx as nx
import matplotlib.pyplot as plt
import operator as op


G = nx.Graph()

""" utility fns for creating digraph """
def add_edge(*args):
    G.add_edges_from(args)
def add_node(n):
    G.add_node(n)

""" fns for counting triangles and triples """
# n choose r, from http://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
def nCr(n, r):
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


if __name__=="__main__":
    edgedef = False # start in "node insertion" mode

    # iterate over stdin
    for line in sys.stdin:
        # filter out section "headers", switch state if necessary, and check
        # to be sure 'base' isn't used as a node
        if "def" in line:
            edgedef = "edge" in line
            continue
        elif "base" in line:
            raise Exception("There's a node named base! Should change.")

        # add nodes or edges based on state
        if not edgedef:
            add_node(line.strip())
        else: # edgedef true
            add_edge(line.strip().split(','))
            
    # now that friends have been added, add base user
    G.add_edges_from([('base', friend) for friend in G.nodes()])


    #nx.draw_graphviz(G)
    #plt.show()
    #print count_triples('base', G)
    print "Cl:\t", Cl(G)
    print "Cl_avg:\t",Cl_avg(G)
    print "Cl_i:\t",Cl_i('base', G)
