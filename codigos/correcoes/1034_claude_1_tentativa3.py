import sys
from collections import deque

def solve(coins, M):
    if M == 0:
        return 0
    dist = [-1] * (M + 1)
    dist[0] = 0
    dq = deque([0])
    coins = sorted(set(coins), reverse=True)
    while dq:
        node = dq.popleft()
        d = dist[node] + 1
        for c in coins:
            nxt = node + c
            if nxt > M:
                continue
            if dist[nxt] == -1:
                dist[nxt] = d
                if nxt == M:
                    return d
                dq.append(nxt)
    return dist[M]

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
        results.append(str(solve(coins, M)))
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    main()