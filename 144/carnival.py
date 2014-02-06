

def rope_game(n):
    # print out expected number of ropes from rope game with n ropes
    val = 0.
    for i in range(n):
        val += 1. / (2*(n-i)-1)
    return val
def rope_game_profit(n):
    return rope_game(n) - n/2.


if __name__=='__main__':
    print rope_game_profit(4)
