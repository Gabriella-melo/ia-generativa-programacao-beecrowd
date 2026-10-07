import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    results = []
    for _ in range(T):
        N = int(data[idx]); M = int(data[idx+1]); idx += 2
        coins = [int(data[idx+i]) for i in range(N)]
        idx += N
        coins = sorted(set(c for c in coins if c <= M))
        INF = float('inf')
        dp = [INF] * (M + 1)
        dp[0] = 0
        for i in range(1, M + 1):
            best = INF
            for c in coins:
                if c > i:
                    break
                if dp[i - c] + 1 < best:
                    best = dp[i - c] + 1
            dp[i] = best
        results.append(str(dp[M]))
    print('\n'.join(results))

if __name__ == "__main__":
    main()