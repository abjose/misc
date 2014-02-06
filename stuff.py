

def dissimilarity(s1, s2):
    # return dissimilarity of two strings
    assert len(s1) == len(s2)
    return sum([1 if s1[i]!=s2[i] else 0 for i in range(len(s1))])

def compare_substrings(n, s1, s2):
    # given two substrings, find all similar-enough matches without shifts
    assert len(s1) == len(s2)
    if n > len(s1):
        return [(s1, s2)]
    matches = []
    i = 0
    while i + n - 1 < len(s1): 
        if dissimilarity(s1[i:i+n], s2[i:i+n]) < n:
            matches.append((s1[i:i+n], s2[i:i+n]))
        i += 1
    return matches
            
def compare_substrings_N(N, s1, s2):
    matches = []
    for n in range(N+1):
        print s1, s2
        matches += compare_substrings(n, s1, s2)
    return matches

def similar_strings(N, S):
    # find substrings that are less than N dissimilar from each other in S
    offset = len(S) - N
    matches = []
    while offset >= 0:
        s1 = S[:len(S)-offset]
        s2 = S[offset:]
        matches += compare_substrings_N(N, s1, s2)
        offset -= 1

    return matches


def k_palindrome(S, k):
    # SHOULD DO SOMETHING WITH EDIT-DISTANCE INSTEAD
    # return True if S is a k-palindrome (can be palindrome if remove at most k
    # characters
    return helper(S, k, 0, len(S)-1)
    
def helper(S, k, head, tail):
    # recursive helper function
    if head >= tail:
        return True
    if k < 0:
        return False
    if S[head] == S[tail]:
        return helper(S, k, head+1, tail-1)
    if S[head] != S[tail]:
        return helper(S, k-1, head, tail-1 ) or helper(S, k-1, head+1, tail)


def magazine_string(S, M):
    # see if can construct string S from character in string M
    mag_dict = dict()
    mag_pointer = 0
    str_pointer = 0

    while True:
        str_char = S[str_pointer]
        mag_char = M[mag_pointer]
        print str_char, mag_char
        if str_char == mag_char:
            # if both equal, don't need to do anything - just move on
            str_pointer += 1
            mag_pointer += 1
        elif str_char in mag_dict.keys() and mag_dict[str_char] > 0:
            # if we've already seen this character, 'use' it
            mag_dict[str_char] -= 1
            str_pointer += 1
        else:
            # if we haven't already seen the character, keep looking
            if mag_char in mag_dict.keys(): mag_dict[mag_char] += 1
            else: mag_dict[mag_char] = 1
            mag_pointer += 1
            
        # check for termination conditions. Make sure to check str first.
        if str_pointer >= len(S):
            return True
        if mag_pointer >= len(M):
            return False

def check_substring(sub, string):
    # see if sub is a substring of string
    # shouldn't go through _every_ substring in string, just until it find right
    # one...
    return any([sub==string[i:i+len(sub)] for i in range(len(string)-len(sub)+1)])

if __name__ == '__main__':
    #print similar_strings(1, "hiphop")
    #print k_palindrome("aaaaasaaaaaaaas", 2)
    #print magazine_string("holere", "hello there")
    print check_substring("bat", "abate")
