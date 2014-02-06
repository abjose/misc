import json
import sys
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
import graph_algs as gralgs #lol


def display_data(G):
    # display all the things for question 2
    # show network graph for fun
    nx.draw_graphviz(G, node_size=30, width=0.5, with_labels=False)
    plt.show()
    # histogram
    gralgs.degree_hist(G, "Log-Histogram of Coauthorship",
                       "Degree", "Log(frequency)")
    # ccdfs
    gralgs.degree_ccdf(nx.DiGraph(G), "CCDF of Coauthorship",
                       "Degree", "Proportion of nodes w/ higher degree")
    # for next operations, going to convert to undirected and convert
    # node labels to integers
    ug = nx.convert_node_labels_to_integers(G)    
    # avg clustering coeff - TREAT AS UNDIRECTED
    print "CL_avg:", gralgs.Cl_avg(ug)
    # overall clustering coeff - TREAT AS UNDIRECTED
    print "CL_overall:", gralgs.Cl(ug)
    # get dists so don't calculate twice
    dists = gralgs.fw_dist(ug)
    # average diameter - TREAT AS UNDIRECTED
    print "Avg diameter:", gralgs.avg_diameter(ug, data=dists)
    # maximal diameter - TREAT AS UNDIRECTED
    print "Maximal diameter:", gralgs.max_diameter(ug, data=dists)

if __name__=='__main__':
    # load json from stdin
    data = json.load(sys.stdin, parse_int=True)

    # convert everything to integers because unicode is annoying to look at
    for k in data.keys():
        data[int(k)] = map(int,data.pop(k))

    # load into the graph
    G = nx.Graph(data)

    # display things for set
    display_data(G)
