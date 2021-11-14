import sys
import pprint
from nbrgen import nbrgen
from b_smooth_check import prime_factorization, read_factor_base, generate_binary_matrix
import numpy as np
from scipy.linalg import lu as lu_factorization
import itertools

def binary_row_reduction(m):
    rows, cols = m.shape
    l = 0
    for k in range(min(rows,cols)):
        if l>= cols: break
        if m[k,l] == 0:
            found_pivot = False
            while not found_pivot:
                if l >= cols: 
                    break
                for i in range(k+1, rows):
                    if m[i,l]:
                        m[[i,k]] = m[[k,i]]
                        found_pivot = True
                        break
                if not found_pivot:
                    l += 1
        if l >= cols: break
        for i in range(k+1, rows):
            if m[i,l]: m[i] ^= m[k]
        l += 1
    return m


if __name__ == '__main__':
    L = 1000
    # L = 10
    d = 5
    F = L - d 
    # Real number: 
    N = 220744554721994695419563
    # Test number:
    # N = 16637
    #Parameter to send in when starting program e.g. python3 main.py <N>
    # N = int(sys.argv[1])
    b_smooth_factors = []
    b_smooth_numbers = []
    
    # Reads prime facor base up to B
    primes = read_factor_base(F)
    
    counter = 0
    while len(b_smooth_factors) < L:
        number = nbrgen(N, counter)
        factors = prime_factorization(number^2 % N, primes)
        if bool(factors):
            # Check if it's a factor of 2 of an already
            # existing factorization
            factors_cp = factors.copy()
            if factors_cp.get(2):
                if factors_cp[2] == 1:
                    del factors_cp[2]
                else:
                    factors_cp[2] -= 1
            if factors_cp in b_smooth_factors:
                print(f"found linear dependency {number}")
                continue
            print(f"found {number}")
            b_smooth_factors.append(factors)
            b_smooth_numbers.append(number)
        else:
            print(f"not b-smooth {number}")
        counter += 1
    print(b_smooth_factors) 
    binary_matrix = np.array(generate_binary_matrix(b_smooth_factors, primes))
    print(binary_matrix)
    """
    This solution doesn't work...
    solutions = binary_row_reduction (binary_matrix)
    """

