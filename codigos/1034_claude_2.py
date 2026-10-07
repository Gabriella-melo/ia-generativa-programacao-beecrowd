import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); m = int(data[idx+1]); idx += 2
        coins = [int(data[idx+i]) for i in range(n)]
        idx += n
        coins = sorted(set(coins))
        INF = float('inf')
        dp = [INF] * (m + 1)
        dp[0] = 0
        for i in range(1, m + 1):
            best = INF
            for c in coins:
                if c > i:
                    break
                v = dp[i - c]
                if v + 1 < best:
                    best = v + 1
            dp[i] = best
        out.append(str(dp[m]))
    print('\n'.join(out))

if __name__ == "__main__":
    main()