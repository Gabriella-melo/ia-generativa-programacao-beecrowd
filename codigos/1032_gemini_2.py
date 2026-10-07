import sys

def main():
    MAX_PRIMES = 3501
    
    # Precompute primes using Sieve of Eratosthenes
    # Upper bound estimate for 3501 primes (using N * log(N) + N * log(log(N)))
    LIMIT = 35000
    is_prime = [True] * LIMIT
    is_prime[0] = is_prime[1] = False
    
    primes = []
    for i in range(2, LIMIT):
        if is_prime[i]:
            primes.append(i)
            if len(primes) == MAX_PRIMES:
                break
            for j in range(i * i, LIMIT, i):
                is_prime[j] = False

    input_data = sys.stdin.read().split()
    results = []

    for item in input_data:
        n = int(item)
        if n == 0:
            break
        
        # 1-based Josephus with varying step sizes (primes)
        ans = 0
        for i in range(1, n + 1):
            p = primes[n - i]
            ans = (ans + p) % i
            
        results.append(str(ans + 1))

    print('\n'.join(results))

if __name__ == '__main__':
    main()
