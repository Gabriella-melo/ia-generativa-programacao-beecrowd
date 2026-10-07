import sys

def mat_mult(a, b, mod):
    return [
        [
            (a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod,
            (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod
        ],
        [
            (a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod,
            (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod
        ]
    ]

def mat_pow(mat, n, mod):
    result = [[1, 0], [0, 1]]

    while n:
        if n & 1:
            result = mat_mult(result, mat, mod)
        mat = mat_mult(mat, mat, mod)
        n >>= 1

    return result

def fibonacci(n, mod):
    if n == 0:
        return 0
    m = mat_pow([[1, 1], [1, 0]], n, mod)
    return m[0][1]

def calls(n):
    # C(0) = C(1) = 1
    # C(n) = C(n-1) + C(n-2) + 1
    # C(n) = 2*F(n+1) - 1
    return n

def solve():
    case = 1

    for line in sys.stdin:
        if not line.strip():
            continue

        n, b = map(int, line.split())

        if n == 0 and b == 0:
            break

        # The number of calls is:
        # C(n) = 2 * F(n+1) - 1
        # Compute it modulo b.
        f = fibonacci(n + 1, b)
        ans = (2 * f - 1) % b

        print(f"Case {case}: {n} {b} {ans}")
        case += 1

if __name__ == "__main__":
    solve()
