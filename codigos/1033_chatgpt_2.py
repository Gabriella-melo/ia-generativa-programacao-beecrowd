import sys

def fib(n, mod):
    if n == 0:
        return 0, 1

    a, b = fib(n >> 1, mod)

    c = (a * ((2 * b - a) % mod)) % mod
    d = (a * a + b * b) % mod

    if n & 1:
        return d, (c + d) % mod
    return c, d


def main():
    case = 1

    for line in sys.stdin:
        if not line.strip():
            continue

        n, base = map(int, line.split())

        if n == 0 and base == 0:
            break

        result, _ = fib(n + 2, base)

        print(f"Case {case}: {n} {base} {result}")
        case += 1


if __name__ == "__main__":
    main()