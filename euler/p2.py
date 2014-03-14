
def fibList(lim):
    fib = []
    a = 0
    b = 1
    while b <= lim:
        fib.append(b)
        c = a+b
        a = b
        b = c
    return fib


evenFib = [f for f in fibList(4e6) if f%2 == 0]
print sum(evenFib)
