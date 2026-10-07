import sys
from itertools import accumulate


def solve(n, m, coins):
    coins = sorted(set(c for c in coins if c <= m))
    if not coins:
        coins = [1]

    INF = m + 1
    dp = [INF] * (m + 1)
    dp[0] = 0

    for c in coins:
        for r in range(c):
            seq = dp[r::c]
            if len(seq) <= 1:
                continue
            newseq = list(accumulate(seq, lambda acc, cur: cur if cur < acc + 1 else acc + 1))
            dp[r::c] = newseq

    return dp[m]


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        coins = [int(x) for x in data[idx:idx + n]]
        idx += n
        out.append(str(solve(n, m, coins)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    main()