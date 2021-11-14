from typing import List, Dict
import math

def read_factor_base(F: int):
    """
    Reads all primes from "prim_2_24.txt" up to value b into a list.
    This list forms the factor base.
    """
    primes = list()
    with open("prim_2_24.txt") as file:
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

def generate_binary_matrix(b_smooth_factors: List[Dict[int, int]], primes: List[int]) -> List[List[int]]:
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

if __name__ == "__main__":
    """
    Test
    """
    primes = read_factor_base(30)
    b_smooth_fact = prime_factorization(24059577777, primes)
    not_b_smooth_fact = prime_factorization(852891037441, primes) # 31^8
    print(f"B-smooth: {b_smooth_fact}")
    print(f"Not B-smooth {not_b_smooth_fact}")
    
