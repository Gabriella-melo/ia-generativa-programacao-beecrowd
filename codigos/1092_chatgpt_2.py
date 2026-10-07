import sys
from bisect import bisect_left

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

        # inc[i][j] = first column >= j where the increasing
        # horizontal run starting at j in row i ends.
        end = [[m] * m for _ in range(n)]

        for i in range(n):
            row = a[i]
            e = m
            for j in range(m - 1, -1, -1):
                if j + 1 < m and row[j] < row[j + 1]:
                    end[i][j] = e
                else:
                    e = j + 1
                    end[i][j] = e

        ans = 1

        # For every possible left column, extend the rectangle
        # downward. For a fixed left column, the largest possible
        # right endpoint is maintained incrementally.
        for left in range(m):
            cur_right = end[0][left]

            if cur_right > left:
                ans = max(ans, cur_right - left + 1)

            height = 1

            for bottom in range(1, n):
                if cur_right <= left:
                    break

                # Horizontal restriction imposed by the new row.
                nr = min(cur_right, end[bottom][left])

                if nr <= left:
                    break

                # The transition from the previous row to the new row
                # requires A[bottom-1][right] < A[bottom][left].
                threshold = a[bottom][left]
                prev = a[bottom - 1]

                # Since prev is increasing only up to cur_right,
                # binary search for the first value >= threshold.
                lo = left
                hi = nr
                while lo < hi:
                    mid = (lo + hi) // 2
                    if prev[mid] < threshold:
                        lo = mid + 1
                    else:
                        hi = mid

                nr = lo

                if nr <= left:
                    break

                cur_right = nr
                height += 1
                area = height * (cur_right - left)
                if area > ans:
                    ans = area

        # Also process rectangles of height 1 efficiently.
        for i in range(n):
            best = 1
            run = 1
            row = a[i]
            for j in range(1, m):
                if row[j - 1] < row[j]:
                    run += 1
                else:
                    run = 1
                if run > best:
                    best = run
            if best > ans:
                ans = best

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()