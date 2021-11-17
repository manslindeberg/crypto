import itertools
import numpy as np
import math as math
import sys
import subprocess
import time
from typing import List, Dict
import sys
from fractions import gcd

"""

█▀▄▀█ █▀▀ █▀▀ ▄▀█   █▀▀ ▄▀█ █▀▀ ▀█▀ █▀█ █▀█ █ ▀█ █▀▀ █▀█
█░▀░█ ██▄ █▄█ █▀█   █▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ █ █▄ ██▄ █▀▄

by Ludvig Lifting & Måns Lindeberg
"""

def generate_binary_matrix(b_smooth_factors: List[Dict[int, int]], primes: List[int]) -> List[List[int]]:
    """
    Generates a binary matrix where each prime factor with
    odd exponent is translated to 1 and 0 for even prime factors.
    """
    binary_matrix = []
    for factors in b_smooth_factors:
        row = [0 for col in range(len(primes))]
        for prime, exponent in factors.items():
            if exponent % 2 == 1:
                row[primes.index(prime)] = 1
        binary_matrix.append(row)
        # print(f"row {row}")
        # print(f"factors {factors}")
    return binary_matrix


def nbrgen(N, start=1):
    """
    Parameters k,j are the upper bounds of k and j
    M is the number to be factorized
    n is the amount of numbers to be generated
    start is the starting number
    """
    k = 1

    while start > int(float(math.sqrt(k * N))):
        k += 1
    
    j = start % int(float(math.sqrt(k * N)))

    return int(float(math.sqrt(k * N) + j))


def nth_root(x, n):
    """
    Functions for taking the integer n:th root of an arbitrary big number
    """
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1


def read_factor_base(F: int):
    """
    Reads all primes from "prim_2_24.txt" up to value b into a list.
    This list forms the factor base.
    """
    primes = list()
    with open("../prim_2_24.txt") as file:
        for line in file:
            line = line.split()
            line = list(map(int, line))
            primes += line
            
            if len(primes) > F:
                break
        
        while len(primes) > F:
                del primes[-1]
    return primes


def prime_factorization(number: int, factor_base: List[int]) -> Dict[int, int]:
    """
    Tries to factorize number using primes from factor_base. If possible, then
    number is a B-smooth number and the factors are returned as a dictionary
    with prime-exponent pairs. If not possible, an empty dictionary is returned.
    """
    prime_factors = dict()
    for prime in factor_base:
        if prime <= number:
            while (number / prime).is_integer():
                if prime in prime_factors:
                    prime_factors[prime] += 1
                else:
                    prime_factors[prime] = 1
                number /= prime
        if number == 1:
            return prime_factors
    else:
        return {}


if __name__ == '__main__':
    """
    MAIN FUNCTION
    """
    start = time.time()
    if len(sys.argv) < 4:
        print("Too few arguments")
        sys.exit()

    N = int(sys.argv[1]) # Number to factorize
    L = int(sys.argv[2]) # Number of B-smooth numbers
    d = int(sys.argv[3]) # Difference between Number of B-smooth numbers and size of factor base
    F = L - d            # Factor base size

    print("Number to factorize: " + str(N) + " ; L = " + str(L) +  " ; F = " + str(F))

    # Declarations
    p = 0
    q = 0
    b_smooth_factors = []
    b_smooth_numbers = []
    b_smooth_numbers_set = set()

    # Reads first F prime numbers
    primes = read_factor_base(F)

    # Generate L B-smooth r^2 numbers
    k = 1
    j = 1
    while len(b_smooth_factors) < L:
        root = math.sqrt(k*N)
        number = int(root) + j
        factors = prime_factorization((number**2) % N, primes)
        if bool(factors):
            # Check if it's a factor of 4 of an already existing factorization
            if  number/2 in b_smooth_numbers_set:
                print(f"Found copy {number} of {int(number/2)}")
            else:
                b_smooth_factors.append(factors)
                b_smooth_numbers.append(number)
                b_smooth_numbers_set.add(number)
        if j % 2 == 0:
            k += 1
        else:
            j += 1

    # Generate Binary matrix & convert to NumPy Array
    binary_matrix = np.array(generate_binary_matrix(b_smooth_factors, primes))
    np.savetxt('binary_matrix.txt', binary_matrix, delimiter=' ', fmt="%d")
    with open("binary_matrix.txt", "r") as f:
        contents = f.readlines()

    # Insert size MxN of binary matrix in first row
    contents.insert(0, str(L) + " " + str(F) + '\n')
    with open("binary_matrix.txt", "w") as f:
        contents = "".join(contents)
        f.write(contents)

    # Execute Binary Solver 
    subprocess.call(["./GaussBin.exe", 'binary_matrix.txt', 'solution.out'])
    with open('solution.out') as f:
        solution = f.readlines()
        for row_index, row in enumerate(solution):
            row = row.split(" ")
            factor_indexes = []
            for bit_index, bit in enumerate(row):
                if(bit == '1'):
                    factor_indexes.append(bit_index)
            number_result = 1
            factor_result = 1
            for i in factor_indexes:
                number_result *= b_smooth_numbers[i]
                for prime,exp in b_smooth_factors[i].items():
                    factor_result *= prime**exp

            factor_result = nth_root(factor_result, 2) % N
            number_result = int(number_result) % N

            if factor_result < number_result:
                gcd = math.gcd(N - (number_result - factor_result), N)
            else:
                gcd = math.gcd(factor_result - number_result, N)

            if(gcd != 1 and gcd != N):
                p = gcd
                q = int(N/p)
                print("Solution found! \n p = " + str(p) + ", q = " + str(q) + ", p*q = " + str(p*q))
                print(f"Execution time {time.time() - start}s")
                break
            else:
                print("No solution found. p = " + str(p))

