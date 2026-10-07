import sys

def solve():
    input = sys.stdin.readline
    T = int(input())

    for _ in range(T):
        N, M = map(int, input().split())
        coins = list(map(int, input().split()))

        INF = M + 1
        dp = [INF] * (M + 1)
        dp[0] = 0

        for i in range(1, M + 1):
            best = INF
            for coin in coins:
                if coin > i:
                    continue
                value = dp[i - coin] + 1
                if value < best:
                    best = value
            dp[i] = best

        print(dp[M])

if __name__ == "__main__":
    solve()