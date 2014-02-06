import matplotlib.pyplot as plt
import math as m


def choose(n,k):
    return m.factorial(n) / (m.factorial(k) * m.factorial(n - k))

def p_err(p, M, R):
    sum_all = 0.
    print R
    for k in range(int(m.ceil(R/2.)),int(R)+1):
        print 'k', k
        sum_all += choose(R,k) * (p**k) * (1-p)**(R-k)
    print
    return 1.-(1.-sum_all)**m.log(M,2)

def rate(M, R):
    bits = m.log(M,2)
    return bits / float(bits*R)
        

if __name__=='__main__':
    p = 0.1
    M = 16
    rates = [1,3,5,7,9]

    y_ax1 = [m.log(p_err(p,M,r),10) for r in rates]
    #y_ax1 = [p_err(p,M,r) for r in rates]
    print y_ax1
    x_ax1 = [rate(M,r) for r in rates]

    M = 256
    #y_ax2 = [p_err(p,M,r) for r in rates]
    y_ax2 = [m.log(p_err(p,M,r),10) for r in rates]
    x_ax2 = [rate(M,r) for r in rates]

    plt.plot(x_ax1, y_ax1, 'bo--', label='M = 16')
    plt.plot(x_ax2, y_ax2, 'ro-.', label='M = 256')
    plt.legend(loc='lower right')
    plt.xlabel(r'$rate$')
    plt.ylabel(r'$log_{10} (P_{error})$')
    plt.show()
