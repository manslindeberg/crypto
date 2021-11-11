import sys
from nbrgen import nbrgen
from b_smooth_check import prime_factorization, read_factor_base

if __name__ == '__main__':
    #Parameter to send in when starting program e.g. python3 main.py N
    N = sys.argv[1]

    primes = read_factor_base(30)
    b_smooth_fact = prime_factorization(24059577777, primes)
    not_b_smooth_fact = prime_factorization(852891037441, primes) # 31^8
    print(f"B-smooth: {b_smooth_fact}")
    print(f"Not B-smooth {not_b_smooth_fact}")