

# could make some kind of recursive prime-checking thing...
# just increment from 2, if divisible call fn on both parts
# if not, return?

def prime_fact(n):
    z = 2
    while z**2 <= n:
        if n%z == 0:
            print z
            #z = 2
            n /= z
        else:
            z += 1
    print n

prime_fact(600851475143)
