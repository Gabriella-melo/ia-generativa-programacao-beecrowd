import sys
from bisect import bisect_left

def solve():
    input = sys.stdin.buffer.readline
    out = []

    while True:
        line = input()
        if not line:
            break

        n, m = map(int, line.split())
        if n == 0 and m == 0:
            break

        a = [list(map(int, input().split())) for _ in range(n)]

        # R[i][j] = maximum length of a strictly increasing
        # horizontal sequence starting at (i, j).
        R = [[1] * m for _ in range(n)]

        for i in range(n):
            row = a[i]
            r = R[i]
            for j in range(m - 2, -1, -1):
                if row[j] < row[j + 1]:
                    r[j] = r[j + 1] + 1

        # B[i][j] = maximum width w such that the last element
        # of row i in the selected rectangle is smaller than
        # the first element of row i+1, for a rectangle starting
        # at column j.
        B = [[0] * m for _ in range(max(0, n - 1))]

        for i in range(n - 1):
            prev = a[i]
            cur = a[i + 1]
            rp = R[i]
            b = B[i]

            for j in range(m):
                end = j + rp[j]
                b[j] = bisect_left(prev, cur[j], j, end) - j

        answer = 1

        # For each starting column, consider a path of rows.
        # Each row has capacity R[i][j], and each edge between
        # consecutive rows has capacity B[i][j].
        #
        # At width w, a valid rectangle corresponds exactly to
        # a connected component of rows whose vertex and edge
        # capacities are at least w.
        #
        # Activate vertices/edges in decreasing capacity using DSU.
        for col in range(m):
            items = []

            for i in range(n):
                cap = R[i][col]
                if cap > 0:
                    items.append((cap, 0, i))

            for i in range(n - 1):
                cap = B[i][col]
                if cap > 0:
                    items.append((cap, 1, i))

            items.sort(reverse=True)

            parent = [-1] * n
            size = [0] * n

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            for cap, typ, idx in items:
                if typ == 0:
                    parent[idx] = idx
                    size[idx] = 1
                    if cap > 0:
                        area = cap
                        if area > answer:
                            answer = area
                else:
                    u = idx
                    v = idx + 1

                    if parent[u] != -1 and parent[v] != -1:
                        ru = find(u)
                        rv = find(v)

                        if ru != rv:
                            if size[ru] < size[rv]:
                                ru, rv = rv, ru
                            parent[rv] = ru
                            size[ru] += size[rv]

                            area = cap * size[ru]
                            if area > answer:
                                answer = area

        out.append(str(answer))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
