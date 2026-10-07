import sys

def fib(n, mod):
    if n == 0:
        return 0, 1

    a, b = fib(n // 2, mod)

    c = (a * ((2 * b - a) % mod)) % mod
    d = (a * a + b * b) % mod

    if n % 2 == 0:
        return c, d
    return d, (c + d) % mod


def main():
    case = 1

    for line in sys.stdin:
        if not line.strip():
            continue

        n, b = map(int, line.split())

        if n == 0 and b == 0:
            break

        f, _ = fib(n + 1, b)
        calls = (2 * f - 1) % b

        print(f"Case {case}: {n} {b} {calls}")
        case += 1


if __name__ == "__main__":
    main()