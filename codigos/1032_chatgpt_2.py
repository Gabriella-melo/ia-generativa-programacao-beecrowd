def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    primes = []

    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            if i * i <= limit:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False

    return primes


def joseph(n, primes):
    people = list(range(1, n + 1))
    pos = 0

    for i in range(n - 1):
        pos = (pos + primes[i] - 1) % len(people)
        people.pop(pos)

    return people[0]


def main():
    values = []
    for line in __import__("sys").stdin:
        n = int(line)
        if n == 0:
            break
        values.append(n)

    if not values:
        return

    max_n = max(values)
    primes = sieve(40000)

    out = []
    for n in values:
        out.append(str(joseph(n, primes)))

    print("\n".join(out))


if __name__ == "__main__":
    main()