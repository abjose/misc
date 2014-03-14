
"""
Naive:
Could decrement from a=999, b=999, and have check_palindrome function...
Could also decrement from 999^2 = 998001 and return first palindrome...
see what's faster?
"""

def is_pal(x):
    # expects integer x
    x = str(x)
    return x[0:len(x)//2] == x[::-1][0:len(x)//2] # better way to reverse end?


def pal1():
    a = 998001
    while a > 10000: # assumes 3-digit...
        if is_pal(a): 
            print a
            # also need to check can be divided by integers...
            # DOESN'T WORK!
            return
        a -= 1

def pal2():
    # note - this one is less efficient...to fix, would have to be sure that
    # you found a palindrome with maximal values of a,b
    A = [a*b for a in range(100, 1000) for b in range(100, 1000) if is_pal(a*b)]
    print max(A)
   

pal2()
