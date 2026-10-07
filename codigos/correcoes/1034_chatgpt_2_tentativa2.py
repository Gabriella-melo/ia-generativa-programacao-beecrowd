import sys

def solve():
    input = sys.stdin.readline
    T = int(input())

    for _ in range(T):
        N, M = map(int, input().split())
        coins = list(map(int, input().split()))

        C = max(coins)

        # Transform the problem:
        # Using k blocks of maximum size C, the total deficit is
        # D = k*C - M.
        # Each block of size a contributes a deficit C-a.
        deficits = sorted(set(C - a for a in coins if a != C))

        limit = C * C
        INF = 10**9
        dp = [INF] * (limit + 1)
        dp[0] = 0

        # Minimum number of non-zero deficits needed to obtain each D.
        for d in range(1, limit + 1):
            best = INF
            for x in deficits:
                if x > d:
                    break
                v = dp[d - x] + 1
                if v < best:
                    best = v
            dp[d] = best

        k = (M + C - 1) // C

        while True:
            deficit = k * C - M

            if deficit <= limit and dp[deficit] <= k:
                print(k)
                break

            k += 1

if __name__ == "__main__":
    solve()