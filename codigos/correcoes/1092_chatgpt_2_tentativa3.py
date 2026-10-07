import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    out = []

    while p < len(data):
        n = data[p]
        m = data[p + 1]
        p += 2

        if n == 0 and m == 0:
            break

        a = []
        for _ in range(n):
            a.append(data[p:p + m])
            p += m

        # right[i][j] = exclusive end of the strictly increasing
        # horizontal sequence beginning at (i, j).
        right = [[m] * m for _ in range(n)]

        for i in range(n):
            row = a[i]
            r = m
            for j in range(m - 1, -1, -1):
                if j + 1 < m and row[j] < row[j + 1]:
                    right[i][j] = r
                else:
                    r = j + 1
                    right[i][j] = r

        answer = 1

        # Fix the left column.
        #
        # For a fixed left column, each row has a horizontal capacity w[i].
        # Between row i-1 and row i there is an additional capacity c[i]:
        # the maximum width for which the last element of row i-1 is
        # smaller than the first element of row i.
        #
        # A rectangle spanning consecutive rows is valid for width x iff
        # every involved row has w >= x and every internal transition has
        # c >= x.
        #
        # Process capacities from large to small with DSU. At threshold x,
        # active rows form exactly the valid consecutive-row components,
        # and x * largest_component_size is the best rectangle at that x.

        for left in range(m):
            w = [right[i][left] - left for i in range(n)]

            # c[i] is the transition capacity from row i-1 to row i.
            c = [0] * n

            for i in range(1, n):
                limit = right[i - 1][left]
                value = a[i][left]
                row = a[i - 1]

                lo = left
                hi = limit

                while lo < hi:
                    mid = (lo + hi) >> 1
                    if row[mid] < value:
                        lo = mid + 1
                    else:
                        hi = mid

                c[i] = lo - left

            # Bucket rows by their horizontal capacity and transitions
            # by their vertical capacity.
            row_bucket = [[] for _ in range(m + 1)]
            edge_bucket = [[] for _ in range(m + 1)]

            for i in range(n):
                row_bucket[w[i]].append(i)

            for i in range(1, n):
                if c[i] > 0:
                    edge_bucket[c[i]].append(i)

            parent = list(range(n))
            size = [1] * n
            active = [False] * n

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            largest = 0

            for width in range(m, 0, -1):
                # Activate all rows capable of supporting this width.
                for r in row_bucket[width]:
                    active[r] = True
                    parent[r] = r
                    size[r] = 1
                    if largest < 1:
                        largest = 1

                # Add all valid transitions at this width.
                for i in edge_bucket[width]:
                    x = i - 1
                    y = i

                    if not active[x] or not active[y]:
                        continue

                    rx = find(x)
                    ry = find(y)

                    if rx != ry:
                        if size[rx] < size[ry]:
                            rx, ry = ry, rx

                        parent[ry] = rx
                        size[rx] += size[ry]

                        if size[rx] > largest:
                            largest = size[rx]

                area = width * largest
                if area > answer:
                    answer = area

        out.append(str(answer))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()