import numpy as np
import math

#   Parameters k,j are the upper bounds of k and j
#   N is the number to be factorized
#   M is the amount of numbers to be generated 
def nbrgen(M, N, bias=1):
    k = 1
    j = 1
    j_upper = M*bias
    r = []

    for i in range(1, M):
        if(i < j_upper):
            j = i
        else:
            k += 1
        r.append(int(float(math.sqrt(k * N) + j)))
    return r

if __name__ == '__main__':
    N = 8492001726483902347212384
    print(nbrgen(1000, N))