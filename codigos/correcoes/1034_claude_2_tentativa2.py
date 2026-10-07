import sys
import numpy as np

def solve(n, m, coins):
    coins = sorted(set(coins))
    INF = m + 1  # coin value 1 is always present, so max possible answer is m
    dp = np.full(m + 1, INF, dtype=np.int64)
    dp[0] = 0

    for c in coins:
        if c > m:
            continue
        for r in range(c):
            idx = np.arange(r, m + 1, c)
            seq = dp[idx]
            j = np.arange(len(seq), dtype=np.int64)
            key = seq - j
            running_min = np.minimum.accumulate(key)
            newseq = running_min + j
            better = newseq < seq
            if np.any(better):
                dp[idx[better]] = newseq[better]

    return int(dp[m])


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        coins = [int(data[idx + i]) for i in range(n)]
        idx += n
        out.append(str(solve(n, m, coins)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    main()