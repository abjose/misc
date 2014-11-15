#!/usr/bin/env python
import math
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import cascaded_union
from shapely.affinity import rotate, translate
from descartes.patch import PolygonPatch

"""
TODO
- add function to wrap closure_test that takes rotation and translation
  of object points?
"""

def init_fig(fig, subplot):
    # mostly just ensures consistency between plots
    if not fig: fig = plt.figure()
    ax = fig.add_subplot(subplot)
    xr = [-5, 5]
    yr = [-5, 5]
    ax.set_xlim(*xr)
    ax.set_xticks(range(*xr) + [xr[-1]])
    ax.set_ylim(*yr)
    ax.set_yticks(range(*yr) + [yr[-1]])
    ax.set_aspect(1)
    return (fig, ax)

#def closure_test(obj, bot_pts, r, shrink=True, plot=False, paths=None):
def closure_test(obj_pt, obj_r, bot_pts, r, shrink=True, plot=False, paths=None):
    """ 
    Determine whether an object is caged (in 'object closure') by a set of
    cylindrical robots.

    obj:     object to test for closure
    bot_pts: list of points defining the centers of cylindrical robots
    r:       radius of cylinder robots
    shrink:  if true and no cage found, will test again with smaller bot radii
    plot:    show visual representation of bots, expanded bots, etc. if True
    paths:   path robot has taken (if any)
    """
    # NOTE: returns true ONLY if robots form a cage and 'origin' is within it -
    # if there's a cage but object isn't in it (because, for example, there's 
    # overlap between robots and object) then this will return false. This might
    # be a problem if the object is technically caged, but is also very close 
    # to a robot and position sensing is noisy (in which case it might 
    # not appear caged).

    # NOTE: CURRENTLY ONLY WORKS WITH CIRCULAR OBJECTS

    origin = (obj_pt.x, obj_pt.y)
    origin = Point(origin)
    
    # make obj a Polygon if it isn't
    #if not isinstance(obj, Polygon):
    #    obj = Polygon(obj)
    obj = origin.buffer(obj_r)
        
    # choose 'origin' - heads up for floating point problems
    # If (0,0) in obj, uses that; otherwise just selects first coordinate.
    #origin = (0,0) if (0,0) in obj.exterior.coords else obj.exterior.coords[0]
    #origin = Point(origin)


    # contract obj to a point by expanding bots
    #expanded_bot = rotate(obj, 180, origin).buffer(r)
    expanded_bot = obj.buffer(r)

    # make a list of 'expanded' robots, translated to bot_pts
    bots = [translate(expanded_bot, bx-origin.x, by-origin.y)
            for (bx,by) in bot_pts]

    # get the cascaded union of all the bots
    bot_union = cascaded_union(bots)

    # convert to list if not a multi-polygon
    if isinstance(bot_union, Polygon):
        bot_union = [bot_union]

    # see if any polygon in bot_union 'cages' the origin
    holes = [Polygon(hole) for poly in bot_union for hole in poly.interiors]
    cage = any([hole.contains(origin) for hole in holes])

    if plot:
        """ Display bots and object normally """
        # initialize plot and add robots
        fig, ax = init_fig(None, 121)
        ax.set_title("Bots and object, unexpanded")
        for bot in bot_pts:
            patch = PolygonPatch(Point(bot).buffer(r), facecolor='red')
            ax.add_patch(patch)

        # add object
        patch = PolygonPatch(obj)
        ax.add_patch(patch)
        plt.plot(origin.x, origin.y, 'go')

        # add path
        if paths:
            bot_path = paths[0]
            patch = PolygonPatch(bot_path, facecolor='pink', alpha=0.6)
            ax.add_patch(patch)

        """ Display expanded bots and point object """
        # re-init plot and add (expanded) robots
        _, ax = init_fig(fig, 122)
        ax.set_title("Expanded bots, contracted object")
        for bot in bot_union:
            ax.add_patch(PolygonPatch(bot, facecolor='red'))
            for hole in bot.interiors:
                hole_poly = Polygon(hole)
                ax.add_patch(PolygonPatch(hole_poly, facecolor='grey'))

        # add object point and show plots
        patch = PolygonPatch(obj, alpha=0.4)
        ax.add_patch(patch)
        plt.plot(origin.x, origin.y, 'go')

        # add path
        if paths:
            hole_path = paths[1]
            patch = PolygonPatch(hole_path, facecolor='pink', alpha=0.6)
            ax.add_patch(patch)

        # add some text
        text, col = ('Cage!', 'green') if cage else ('No cage...', 'red')
        ax.text(-1 , 4, text, style='italic',
                bbox={'facecolor':col, 'alpha':0.5, 'pad':10})
        plt.show()

    #if not cage and shrink:
    if False:
        # could change shrink to a number, try that many times...
        eps = 0.05
        #cage = closure_test(obj, bot_pts, r-eps, shrink=False, plot=plot)
        cage = closure_test(obj_pt, obj_r, bot_pts, r-eps, shrink=False, plot=plot)
    return cage
    
def cylinder_closure_test(target, bot_pts, bot_r, 
                          shrink=True, plot=False, paths=None):
    #return closure_test(target.obj, bot_pts, bot_r, shrink, plot, paths)
    return closure_test(target.pose, target.radius, bot_pts, bot_r, 
                        shrink, plot, paths)

def make_cylinder_bot(r, h):
    from polygon_mesh import make_poly_mesh
    pt = Point(0,0)
    p  = pt.buffer(r)
    make_poly_mesh(p.exterior.coords, h)

if __name__ == "__main__":
    # demonstrate closure test
    # cylindrical robot radius
    r = 0.55
    # list of robot locations
    bot_pts = [(-1,-1),
              (-1,1),
              (1,-1),
              (1,1)]

    # list of points defining object exterior
    obj_ext = [(-.350, -.350), # use r=0.55 for closure with this object
               (0, .25), 
               (.5, .75), 
               (.95, 0)]

    # see if enclosed and plot
    #print 'object closure?:', closure_test(obj_ext, bot_pts, r, plot=True)

