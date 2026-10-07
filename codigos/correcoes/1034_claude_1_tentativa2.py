import sys
import numpy as np

def solve_case(coins, M):
    INF = 10**9
    dp = np.full(M + 1, INF, dtype=np.int64)
    dp[0] = 0

    coins = sorted(set(c for c in coins if 1 <= c <= M))

    for a in coins:
        # Process each residue class modulo a.
        # For subsequence dp[r], dp[r+a], dp[r+2a], ...
        # out[k] = min_{j<=k} (temp[j] + (k-j))
        #        = (min_{j<=k} (temp[j]-j)) + k
        for r in range(a):
            idx = np.arange(r, M + 1, a)
            temp = dp[idx]
            offsets = np.arange(len(temp), dtype=np.int64)
            u = temp - offsets
            cummin_u = np.minimum.accumulate(u)
            new_temp = cummin_u + offsets
            dp[idx] = np.minimum(temp, new_temp)

    return int(dp[M])

def main():
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    results = []
    for _ in range(T):
        N = int(data[idx]); M = int(data[idx + 1]); idx += 2
        coins = []
        for i in range(N):
            coins.append(int(data[idx])); idx += 1
        results.append(str(solve_case(coins, M)))
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    main()