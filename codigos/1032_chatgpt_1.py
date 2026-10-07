import sys

MAX_N = 3501

def generate_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    primes = []

    for i in range(2, limit + 1):
        if sieve[i]:
            primes.append(i)
            if i * i <= limit:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False

    return primes

primes = generate_primes(40000)

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
        for i in range(1, n + 1):
            self.bit[i] += 1
            j = i + (i & -i)
            if j <= n:
                self.bit[j] += self.bit[i]

    def add(self, i, value):
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def kth(self, k):
        idx = 0
        bit_mask = 1 << (self.n.bit_length() - 1)

        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            bit_mask >>= 1

        return idx + 1

def solve(n):
    if n == 1:
        return 1

    fw = Fenwick(n)
    remaining = n
    current_rank = 1

    for i in range(n - 1):
        step = primes[i]
        current_rank = (current_rank + step - 1) % remaining + 1

        pos = fw.kth(current_rank)
        fw.add(pos, -1)
        remaining -= 1

        if remaining:
            current_rank = (current_rank - 1) % remaining + 1

    return fw.kth(1)

answers = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    n = int(line)
    if n == 0:
        break

    if n not in answers:
        answers[n] = solve(n)

    print(answers[n])
