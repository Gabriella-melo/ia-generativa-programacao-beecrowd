import sys

def sieve_primes(count):
    # Estimate upper bound for the count-th prime
    if count < 6:
        limit = 15
    else:
        import math
        limit = int(count * (math.log(count) + math.log(math.log(count)))) + 10
    primes = []
    while True:
        sieve = bytearray([1]) * (limit + 1)
        sieve[0] = sieve[1] = 0
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = 0
        primes = [i for i, v in enumerate(sieve) if v]
        if len(primes) >= count:
            return primes[:count]
        limit *= 2

def solve(n, primes):
    if n == 1:
        return 1
    people = list(range(1, n + 1))
    idx = 0
    for i in range(n - 1):
        step = primes[i]
        idx = (idx + step - 1) % len(people)
        people.pop(idx)
    return people[0]

def main():
    lines = sys.stdin.read().split()
    ns = []
    for token in lines:
        val = int(token)
        if val == 0:
            break
        ns.append(val)

    if not ns:
        return

    max_n = max(ns)
    needed_primes = max(0, max_n - 1)
    primes = sieve_primes(needed_primes) if needed_primes > 0 else []

    results = []
    for n in ns:
        results.append(str(solve(n, primes)))

    print("\n".join(results))

if __name__ == "__main__":
    main()