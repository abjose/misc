import matplotlib.pyplot as plt


if __name__=='__main__':
    
    # assume units are Mbps
    CAPACITY = 20.
    # window divider
    ALPHA = 1.1
    alphas = [1.1, 1.2, 1.3, 1.4, 1.5]
    #alphas = [1.1]

    # RTTs in seconds
    t1 = 0.1
    t2 = 0.2

    # windows
    w1 = 1.
    w2 = 1.

    # throughputs
    x1 = 0.
    x2 = 0.

    # time to run things for
    runtime = 100

    x1v, x2v = [], []
    for a in alphas:
        x1v_temp, x2v_temp = [], []
        # simulation loop
        for t in range(runtime):
            # update throughputs
            x1 = w1 / t1
            x2 = w2 / t2

            # update window size
            if x1 + x2 <= CAPACITY:
                w1 += 1.0
                w2 += 0.5
            else:
                w1 /= a
                w2 /= a
        
            x1v_temp.append(x1)
            x2v_temp.append(x2)
            print x1,x2
        x1v.append(x1v_temp)
        x2v.append(x2v_temp)

    plt.xlabel(r'Flow 2 Throughput')
    plt.ylabel(r'Flow 1 Throughput')
    cols = ['r','g', 'b', 'y', 'r']
    for a, b, c in zip(x1v, x2v, cols):
        #plt.plot(x2v, x1v, 'b.')
        print c
        plt.plot(b, a, c+'.')
    plt.show()
