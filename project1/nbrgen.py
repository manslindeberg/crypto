import math

#   Parameters k,j are the upper bounds of k and j
#   M is the number to be factorized
#   n is the amount of numbers to be generated
#   start is the starting number
def nbrgen(N, start=1):
    k = 1
    
    while start > int(float(math.sqrt(k * N))):
        k += 1
    
    j = start % int(float(math.sqrt(k * N)))

    return int(float(math.sqrt(k * N) + j))


if __name__ == '__main__':
    N = 8492001726483902347212384
    print(nbrgen(N,  2914103931997*23))