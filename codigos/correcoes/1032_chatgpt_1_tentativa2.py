import sys

MAX_N = 3501

def generate_primes(count):
    limit = 40000
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    primes = []

    for i in range(2, limit + 1):
        if sieve[i]:
            primes.append(i)
            if len(primes) == count:
                break
            for j in range(i * i, limit + 1, i):
                sieve[j] = False

    return primes

primes = generate_primes(MAX_N)

def solve(n):
    people = list(range(1, n + 1))
    index = 0

    for i in range(n - 1):
        index = (index + primes[i] - 1) % len(people)
        people.pop(index)

        if index == len(people):
            index = 0

    return people[0]

cache = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    n = int(line)

    if n == 0:
        break

    if n not in cache:
        cache[n] = solve(n)

    print(cache[n])