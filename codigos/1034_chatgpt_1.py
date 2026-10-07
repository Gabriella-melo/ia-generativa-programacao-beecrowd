import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        n = data[pos]
        m = data[pos + 1]
        pos += 2

        blocks = data[pos:pos + n]
        pos += n

        # Unbounded coin change: each block type can be used any number of times.
        # Since 1 is always available, every value up to M is reachable.
        dp = [m + 1] * (m + 1)
        dp[0] = 0

        for i in range(1, m + 1):
            best = m + 1
            for a in blocks:
                if a > i:
                    continue
                value = dp[i - a] + 1
                if value < best:
                    best = value
            dp[i] = best

        out.append(str(dp[m]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
