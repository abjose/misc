import numpy as np
import itertools as it

# get all strings of length k of alphabet {1,2,3,4}
def get_strings(k):
    return [''.join(i) for i in it.product("1234",repeat=k)]

# get lesser strings
def get_lesser_strings(s, equal=True):
    strings = get_strings(len(s))
    val = int(s)
    if equal:
        return [st for st in strings if int(st) <= val]
    return [st for st in strings if int(st) < val]

# transition matrix
P = [[5./8, 1./8, 1./8, 1./8],
     [1./8, 5./8, 1./8, 1./8],
     [1./8, 1./8, 5./8, 1./8],
     [1./8, 1./8, 1./8, 5./8]]

# get prob of string
def string_prob(s):
    prob = .25
    for i in range(len(s)-1):
        curr = int(s[i+1])
        prev = int(s[i])
        prob *= P[curr-1][prev-1]
    return prob

# sum probs over set of strings
def sum_lesser(s, equal=True):
    S = get_lesser_strings(s, equal)
    probs = 0.
    for s in S:
        probs += string_prob(s)
    return probs


if __name__=='__main__':
    #print len(get_lesser_strings("33222"))
    print string_prob("33222")
    print string_prob('33222')
    print sum_lesser("33222", equal=False) + string_prob('33222')/2.
