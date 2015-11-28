import sys

def make_poly_mesh(obj_pts, height):
    # make .tri file of given polygon with given height
    # if last if duplicate of first
    if obj_pts[0] == obj_pts[-1]:
        obj_pts = obj_pts[:-1]

    # find vertices
    v_lo = [(x,y,0)      for (x,y) in obj_pts]
    v_hi = [(x,y,height) for (x,y) in obj_pts]
    vertices = [v for vs in zip(v_lo, v_hi) for v in vs]

    # find triangles
    n = len(obj_pts)
    walls   = [(i, (i+1)%(2*n), (i+2)%(2*n)) for i in range(0,2*n,2)]
    walls  += [(i, (i+2)%(2*n), (i+1)%(2*n)) for i in range(1,2*n,2)]
    floor   = [(0, 2*i+2, 2*i) for i in range(1,n-1)]
    ceiling = [(1, 2*i+3, 2*i+1) for i in range(1,n-1)]
    triangles = walls+floor+ceiling

    assert(len(vertices) == 2*n)
    assert(len(triangles) == 4*n-4)

    # print to stdout in .tri format
    sys.stdout.write(str(2*n) + "\n")
    sys.stdout.write("\n".join(map(" ".join, [map(str,v) for v in vertices])))
    sys.stdout.write("\n" + str(4*n-4) + "\n")
    sys.stdout.write("\n".join(map(" ".join, [map(str,t) for t in triangles])))
    sys.stdout.write("\n")


if __name__=='__main__':

    obj_ext = [(-1.25,  0.25), # use r=0.75 for closure
               (-0.25, 2.25),
               (-0.25, -0.25),
               (0.25, -0.25)]

    square = [(0,0),
              (0,1),
              (1,1),
              (1,0)]
              
    square2 = [(-.350, -.350), # use r=0.55 for closure
               (0, .25), 
               (.5, .75), 
               (.95, 0)]
              
    concave = [(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)]

    #make_poly_mesh(square, 1)
    #make_poly_mesh(obj_ext, 1)
    make_poly_mesh(square2, .5)


