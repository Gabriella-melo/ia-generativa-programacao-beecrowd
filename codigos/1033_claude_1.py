import sys

def fib_pair(k, m):
    if k == 0:
        return (0, 1)
    a, b = fib_pair(k >> 1, m)
    c = (a * ((2 * b - a) % m)) % m
    d = (a * a + b * b) % m
    if k & 1:
        return (d, (c + d) % m)
    else:
        return (c, d)

def solve():
    data = sys.stdin.read().split()
    idx = 0
    case = 1
    out = []
    while idx + 1 < len(data):
        n = int(data[idx]); b = int(data[idx+1]); idx += 2
        if n == 0 and b == 0:
            break
        f = fib_pair(n + 1, b)[0]
        ans = (2 * f - 1) % b
        out.append(f"Case {case}: {n} {b} {ans}")
        case += 1
    sys.stdout.write("\n".join(out) + "\n")

solve()