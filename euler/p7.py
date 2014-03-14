# What is the 10 001st prime number?
# just make a sieve and then play around until get 10001?

import math as m

def sieve(n):
    # sieve of eratosthenes on [1..n)
    # use a 2nd 'mirror list' to mark inclusion in final list
    #nums = range(3,n,2) # skip even numbers
    marks = [True]*(n+1)
    marks[0] = marks[1] = False
    primes = []
    
    for (i,isPrime) in enumerate(marks):
        # generate factors
        if isPrime:
            primes.append(i)
            for n in xrange(i*i, n+1, i):
                marks[n] = False

    # could make a generator...
    return primes

print sieve(100)
    

# NOT DONE!!
