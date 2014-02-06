from fetcher import fetch_links
import networkx as nx
import matplotlib.pyplot as plt
import graph_algs as gralgs
# all for non-blocking user input...
import sys
import select
import tty
import termios

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def display_data():
    # display all the things for question 3, assume G is target graph
    global G
    # show network graph for fun
    nx.draw_graphviz(nx.Graph(G), node_size=10, width=0.4, with_labels=False)
    plt.show()
    # histogram for in and out links
    gralgs.degree_hist(G, "Log-Histogram of Hyperlinks per page",
                       "Degree", "Log(frequency)")
    gralgs.degree_hist(G, "Log-Histogram of Hyperlinks pointing to a page",
                       "Degree", "Log(frequency)", out=False)
    # ccdfs for in and out links
    gralgs.degree_ccdf(G, "CCDF of Hyperlinks per page",
                       "out-degree", "Proportion of nodes w/ higher out-degree")
    gralgs.degree_ccdf(G, "CCDF of Hyperlinks pointing to a page",
                       "in-degree", "Proportion of nodes w/ higher in-degree",
                       out=False)
    # for next operations, going to convert to undirected and convert
    # node labels to integers
    ug = nx.convert_node_labels_to_integers(nx.Graph(G))    
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
    # wait to make sure we saw everything
    raw_input('Press enter to continue...')
    

# declare global link graph
G = nx.DiGraph()
crawled = set()

def fmap(flist, arg):
    # apply list of functions to argument
    res = arg[:]
    for f in flist: res = f(res)
    return res

def filter_links(rules, links):
    return fmap(rules, links)

def in_caltech():
    return [lambda links: [l for l in links if 'caltech.edu' in l]]

def is_text():
    # a little coarse...could switch to only check ending
    # better to just verify ending is .html or /???
    banned = ['.jpeg','.jpg','.png','.pdf','.ps','.gz','.rpm','.md5','.iso',
              '.xml','.TBL','.img','.bz2','.cat','.msg','.cfg','.lss']
    return [lambda links: [l for l in links 
                           if not any([n in l for n in banned])]]
def not_crawled():
    global crawled
    return [lambda links: [l for l in links if l not in crawled]]

def not_in_graph():
    global G
    return [lambda links: [l for l in links if l not in G]]

def get_next_seed(links):
    seed = None
    potential_seeds = set(links[:])
    while not seed and potential_seeds:
        temp_seed = potential_seeds.pop()
        try:    fetch_links(temp_seed)
        except: continue
        seed = temp_seed
    return seed # make sure to check if None

def crawl_recursive(seed):
    global G, crawled
    
    print 'seed:', seed
    print "nodes:", len(G)
    crawled |= {seed}
    # Fetch links for seed if possible. If exception, do nothing
    links = []
    try: 
        links = filter_links(in_caltech() + not_crawled() + is_text(),
                             fetch_links(seed))
    except Exception, e: 
        print 'got exception:', e
        return #exit(1)
    # filter links
    # if have no links left, return
    if not links: 
        G.add_node(seed)
        return # can check somewhere else?
    # add remaining links to graph
    G.add_edges_from([(seed, l) for l in links])
    # then call crawl_recursive on each
    map(crawl_recursive, links)

    # could change selection policy - like look for nodes that might have high
    # degree?
    # could change to adding links to a queue, which is processed
    # by multiple threads?
    # TODO: could change selection alg to being unexplored node in current graph
    #       with highest in-degree? Or could try go get pagerank

    # generate graphs if g is pressed
    if isData():
        c = sys.stdin.read(1)
        if c == "g":
            # TODO: generate data here
            print 'got here!'
            display_data()


def crawl_pagerank():
    # do a crawl with pagerank-based selection policy
    global G, crawled
    seed = 'http://www.caltech.edu/'
    links = []

    while True:
        print 'seed:',seed
        print 'nodes:',len(G)
        # indicate seed has been crawled
        crawled |= {seed}
        G.add_node(seed)
        
        # populate graph with results from current seed
        try: 
            links = filter_links(in_caltech() + not_crawled() + is_text(),
                                 fetch_links(seed))
        except Exception, e: 
            print 'GOT EXCEPTION:', e
            links = []
            #continue
        if links: 
            G.add_edges_from([(seed, l) for l in links])  # add links if found

        # choose new seed based on highest pagerank node in current graph
        seed = gralgs.highest_pagerank_node(G,crawled)
        if seed == None:
            # if no node found, stop...
            print "Can't find a good seed, stopping  crawl."
            # graph things here?
            return

        # generate graphs if g is pressed
        if isData():
            c = sys.stdin.read(1)
            if c == "g":
                # TODO: generate data here
                print 'got here!'
                display_data()
            

# TODO: Should run both with 'take-first' and pagerank and see how different
# TODO: split code up into sections - put each in folder?

if __name__=="__main__":

    #G.add_nodes_from(fetch_links('http://www.caltech.edu/'))
    #print len(filter_links(fetch_links('http://www.caltech.edu/')))
    #crawl()

    # crawl, if q is pressed then generate figures and data
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    #crawl_recursive('http://www.caltech.edu/')
    crawl_pagerank()
