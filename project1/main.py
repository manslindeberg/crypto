import sys
import pprint
from nbrgen import nbrgen
from b_smooth_check import prime_factorization, read_factor_base

if __name__ == '__main__':
    #Parameter to send in when starting program e.g. python3 main.py <N>
    N = int(sys.argv[1])
    b_smooth_fact = []
    primes = read_factor_base(30)
    print(primes)

    counter = 0
    while len(b_smooth_fact) < 1000:
        nbr = nbrgen(N, counter)
        factor = prime_factorization(nbr, primes)
        if bool(factor):
            b_smooth_fact.append(nbr)
        counter += 1
    print(b_smooth_fact)