from itertools import combinations

"""
Convenience functions for configurations

"""


def get_neighbors(c):
    # return a list of the configuration 'neighbors' of c - distance 1 away
    # if define other functions in terms of this, should be easy to modify
    # to allow changing number of robots...
    # ASSUMES 4-CONNECTED
    # for each element, modify by one in each direction
    c = list(c)
    neighbors = []
    for (bi,bj) in c:
        # for each bot, perturb in each direction...
        c_less_b = [b for b in c if b != (bi,bj)]
        neighbors.append(tuple([(bi-1,bj-1)] + c_less_b))
        neighbors.append(tuple([(bi  ,bj+1)] + c_less_b))
        neighbors.append(tuple([(bi+1,bj  )] + c_less_b))
        neighbors.append(tuple([(bi+1,bj+1)] + c_less_b))
    # remove invalid neighbors in a cringe-worthy way
    neighbors = set([tuple(sorted(set(n))) for n in neighbors 
                     if len(set(n)) == len(c)])
    return neighbors

def get_all_configurations(r, n):
    # return all possible n-robot configurations on an r-radius grid
    # THIS ISN'T REALLY NECESSARY...
    return combinations(generate_grid(r), n)

def generate_grid(r):
    # return all grid points in r-radius square grid centered on (0,0)
    # probably won't have to use this either
    vals = range(-r,r+1)
    return [(m,n) for m in vals for n in vals]



if __name__=='__main__':
    #s = get_all_configurations(1, 3)
    
    c = ((0,0), (1,1))
    print get_neighbors(c)
