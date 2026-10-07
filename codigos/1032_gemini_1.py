import sys

def precompute_primes(limit):
    is_prime = [True] * limit
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, limit):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, limit, i):
                is_prime[j] = False
    return primes

primes = precompute_primes(40000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ans = []
    for line in input_data:
        n = int(line)
        if n == 0:
            break
        
        pos = 0
        for i in range(2, n + 1):
            p = primes[n - i]
            pos = (pos + p) % i
            
        ans.append(str(pos + 1))
        
    print('\n'.join(ans))

if __name__ == '__main__':
    solve()
