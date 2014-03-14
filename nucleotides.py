
"""
Code from an interview
Main goal is to test for errors in returned list of nucleotides
"""

from collections import defaultdict

d = dict(A='T', T='A', C='G', G='C')
def complement(c):
    return d[c]

def rev_comp(s):
    a = [complement(c) for c in s]
    return ''.join(a[::-1]).upper()

def strand_hamming(s1, s2):
    assert(len(s1) == len(s2))
    return sum([1 if c1 != c2 else 0 for c1,c2 in zip(s1,s2)])

def normalize_strand(s):
    return min(s, rev_comp(s))

def nucleotide_correction_map(S):
    # count normalized strands
    norm_counts = defaultdict(int)
    # store map of corrections
    corrections = dict()

    for strand in S:
        norm_counts[normalize_strand(strand)] += 1
    
    # precalculate lists of valid and invalid strands
    invalids = [k for k,v in norm_counts.items() if v == 1]
    valids   = [k for k,v in norm_counts.items() if v > 1]
    
    # find mapping from invalids to valids
    for invalid in invalids:
        # get the correct form of the invalid strand
        true_invalid = invalid if invalid in S else rev_comp(invalid)
        for valid in valids:
            # get the correct form of the valid strand (if both forms present,
            # doesn't really matter)
            true_valid = valid if valid in S else rev_comp(valid)
            # see if valid is a correction for invalid
            dist   = strand_hamming(true_invalid, true_valid)
            dist_c = strand_hamming(true_invalid, rev_comp(true_valid))
            if dist == 1 or dist_c == 1:
                # add correction to the map and keep going
                corrections[true_invalid] = true_valid
                break
        # raise an exception if there was no correction for this strand
        if true_invalid not in corrections.keys():
            raise Exception("No correction found for strand " + true_invalid)

    return corrections

# a<->t
# c<->g

if __name__=="__main__":
    """
    Cases to test for:
    - strands counted properly with their rev_comps
    - valid   strand stored as its rev_comp is properly recovered (if necessary)
    - invalid strand stored as its rev_comp is properly recovered
    - Exception raised if no correction exists
    """
    strands = ['ATCG',
               'ATCG',
               'CGAA',
               'ATCT',
               'ATCA',
               'AGAT',
               'GGGG',
               'GGGG',
               'CCCA']
    print nucleotide_correction_map(strands)
