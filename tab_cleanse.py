#!/usr/bin/env python2.5

"""
I use the 'OneTab' chrome extension to keep my tab-collecting habits in check. This is a script to read in my saved tabs from stdin, remove duplicates, and spit them back out to stdout.

"""

import sys
import collections

if __name__=='__main__':
    # need to maintain ordering
    s = collections.OrderedDict([(l,None) for l in sys.stdin])
    sys.stdout.write(''.join(s.keys()))
