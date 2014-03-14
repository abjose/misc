import numpy as np

# want sum of all multiples of 3 or 5:

odds = range(1000)
final = []
for i in odds:
    if i % 3 == 0 or i % 5 == 0:
        final.append(i)
print sum(final)
