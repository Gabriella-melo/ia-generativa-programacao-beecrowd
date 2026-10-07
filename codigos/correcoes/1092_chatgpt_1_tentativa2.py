import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline
    ans = []

    while True:
        line = input()
        if not line:
            break

        n, m = map(int, line.split())
        if n == 0 and m == 0:
            break

        a = [list(map(int, input().split())) for _ in range(n)]

        # inc[i][j] = maximum width of a strictly increasing
        # sequence starting at (i, j).
        inc = [[1] * m for _ in range(n)]

        for i in range(n):
            row = a[i]
            dp = inc[i]
            for j in range(m - 2, -1, -1):
                if row[j] < row[j + 1]:
                    dp[j] = dp[j + 1] + 1

        best = 1

        # For every possible left column, each row is a vertex
        # with capacity inc[i][left].
        #
        # Between row i and i+1, the edge capacity is the maximum
        # width w for which:
        #
        # a[i][left+w-1] < a[i+1][left]
        #
        # Since row i is increasing over inc[i][left] positions,
        # this capacity is found by binary search.
        for left in range(m):
            vertices = []
            edges = []

            for i in range(n):
                vertices.append((inc[i][left], i))

            for i in range(n - 1):
                limit = inc[i][left]
                right = left + limit
                # Number of positions whose value is < a[i+1][left].
                edge_cap = bisect_left(
                    a[i], a[i + 1][left], left, right
                ) - left
                edges.append((edge_cap, i))

            # Process capacities in decreasing order.
            # Vertices MUST be activated before edges having
            # the same capacity.
            events = []

            for cap, i in vertices:
                events.append((cap, 0, i))

            for cap, i in edges:
                if cap > 0:
                    events.append((cap, 1, i))

            events.sort(key=lambda x: (-x[0], x[1]))

            parent = [-1] * n
            size = [0] * n

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            for cap, typ, idx in events:
                if typ == 0:
                    parent[idx] = idx
                    size[idx] = 1

                    area = cap
                    if area > best:
                        best = area
                else:
                    u = idx
                    v = idx + 1

                    if parent[u] == -1 or parent[v] == -1:
                        continue

                    ru = find(u)
                    rv = find(v)

                    if ru != rv:
                        if size[ru] < size[rv]:
                            ru, rv = rv, ru

                        parent[rv] = ru
                        size[ru] += size[rv]

                        area = cap * size[ru]
                        if area > best:
                            best = area

        ans.append(str(best))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()