import sys

def fib_mod(n, m):
    def fd(k):
        if k == 0:
            return (0, 1)
        a, b = fd(k >> 1)
        c = (a * ((2 * b - a) % m)) % m
        d = (a * a + b * b) % m
        if k & 1:
            return (d, (c + d) % m)
        else:
            return (c, d)
    return fd(n)[0]

def main():
    data = sys.stdin.read().split()
    idx = 0
    case = 1
    out = []
    while idx + 1 < len(data) or idx < len(data):
        if idx >= len(data):
            break
        n = int(data[idx]); b = int(data[idx+1])
        idx += 2
        if n == 0 and b == 0:
            break
        fib_val = fib_mod(n + 1, b)
        result = (2 * fib_val - 1) % b
        out.append(f"Case {case}: {n} {b} {result}")
        case += 1
    print("\n".join(out))

if __name__ == "__main__":
    main()