
"""
Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

Doing the naive way first...
"""


sumsq = 0
sqsum = 0
for i in range(1,101):
    sqsum += i
    sumsq += i**2
print sqsum**2 - sumsq


# better, but still naive - can pair things in sum
# like 100, 99+1, 98+2 -- end up with 100*50 for sum
# still have to loop for squares...

# also fancy ways to do without looping at all, see project euler thread 6
