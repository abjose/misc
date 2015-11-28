
"""
- take in object description, number of robots(?), grid spacing, radius(?)
- generate every possible configuration (ignoring dupes) of pegs
- NOTE: will need to make sure robot centers translate to pegs...
- for each unique configuration, test for closure and create a relevant tuple
- store tuple in some kind of...tuplestore.

- consider using some NoSQL database
- SPACING WILL ONLY BE USED WHEN trying to convert from real world to grid?
- honestly wouldn't it be better to only test out configurations that
  you're actually going to try? like as you look at a path, etc.
- do you really even need to keep track of a grid at all? Just need 
  to remember grid spacing for doing conversions...
"""


def test_configuration(c):
    # return true if configuration c yields closure
    # if already calculated, use that value...otherwise calculate and store.
    # use mongodb?
    pass

def get_safety(c):
    # calculate the 'distance' to an unsafe configuration from this one
    # returns 0 if this configuration is unsafe
    # 1 means 1 movement (of any robot to any peg) away, 2 is 2 movements, etc.
    # right now only considers bot movements (not additions/subtractions)
    safety = 0
    active = {c}
    
    while True:
        new_active = set() # set for next round
        for c2 in active:
            # if not safe, have determined safety of c so return
            if not test_configuration(c2): return safety
            # otherwise add neighbors to set for next round
            new_active |= get_neighbors(c2)
        # didn't find an unsafe configuration, proceed to next round
        active = new_active
        safety += 1
    
    assert(False) # huh

def get_safe_path(ci, cg, s):
    # find a safe path from ci to cg while maintaining safety >= s
    # basically A*, treats too un-safe configurations as 'walls'
    # A* pseudocode stolen from wikipedia A* page
    closedset = set() # The set of nodes already evaluated.
    openset = {ci}    # The set of tentative nodes to be evaluated
    came_from = the empty map    # The map of navigated nodes.
 
    g_score[start] = 0    # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal)
 
    while openset is not empty
        current = the node in openset having the lowest f_score[] value
        if current == goal:
            return reconstruct_path(came_from, goal)
 
        remove current from openset
        add current to closedset
        for each neighbor in neighbor_nodes(current):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + dist_btwn(current,neighbor)
 
            if neighbor not in openset or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                if neighbor not in openset:
                    add neighbor to openset
 
    return failure
 
def reconstruct_path(came_from, current_node):
    if current_node in came_from:
        p = reconstruct_path(came_from, came_from[current_node])
        return (p + current_node)
    else:
        return current_node


if __name__=='__main__':
    pass
