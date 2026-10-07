import sys

def sieve_primes(limit):
    is_composite = bytearray(limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if not is_composite[i]:
            primes.append(i)
            for j in range(i * i, limit + 1, i):
                is_composite[j] = 1
    return primes

MAX_PRIMES_NEEDED = 3600
LIMIT = 50000
primes = sieve_primes(LIMIT)
while len(primes) < MAX_PRIMES_NEEDED:
    LIMIT *= 2
    primes = sieve_primes(LIMIT)

def solve(n):
    if n == 1:
        return 1
    people = list(range(1, n + 1))
    idx = 0
    for i in range(n - 1):
        m = primes[i]
        idx = (idx + m - 1) % len(people)
        people.pop(idx)
        if len(people) > 0:
            idx = idx % len(people)
    return people[0]

def main():
    results = []
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue
        n = int(line)
        if n == 0:
            break
        results.append(str(solve(n)))
    print('\n'.join(results))

if __name__ == '__main__':
    main()