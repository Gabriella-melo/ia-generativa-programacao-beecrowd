import sys
from bisect import bisect_left

def largest_histogram(h):
    stack = []
    best = 0
    n = len(h)

    for i in range(n + 1):
        cur = h[i] if i < n else 0

        while stack and h[stack[-1]] >= cur:
            height = h[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            area = height * (i - left)
            if area > best:
                best = area

        stack.append(i)

    return best


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    out = []

    while pos < len(data):
        n = data[pos]
        m = data[pos + 1]
        pos += 2

        if n == 0 and m == 0:
            break

        a = []
        for _ in range(n):
            a.append(data[pos:pos + m])
            pos += m

        # end[i][j] is the exclusive right boundary of the
        # strictly increasing horizontal segment starting at (i,j).
        end = [[m] * m for _ in range(n)]

        for i in range(n):
            row = a[i]
            right = m
            for j in range(m - 1, -1, -1):
                if j + 1 < m and row[j] < row[j + 1]:
                    end[i][j] = right
                else:
                    right = j + 1
                    end[i][j] = right

        answer = 1

        # Fix the left column. For every row, compute the maximum
        # width that can participate in a rectangle whose left
        # boundary is this column.
        #
        # These widths form a histogram: for any consecutive group
        # of rows, the largest possible rectangle width is the
        # minimum width in that group. Thus the largest rectangle
        # in the histogram gives the best rectangle for this left
        # column.
        for left in range(m):
            heights = [0] * n

            heights[0] = end[0][left] - left

            for i in range(1, n):
                current_end = end[i][left]
                previous_end = end[i - 1][left]

                limit = min(current_end, previous_end)

                if limit <= left:
                    heights[i] = 0
                    continue

                value = a[i][left]
                prev_row = a[i - 1]

                # First position in the previous row whose value
                # is >= value. The previous row is strictly
                # increasing from 'left' up to previous_end.
                lo = left
                hi = limit

                while lo < hi:
                    mid = (lo + hi) // 2
                    if prev_row[mid] < value:
                        lo = mid + 1
                    else:
                        hi = mid

                # The right endpoint must be strictly before lo.
                heights[i] = lo - left

            area = largest_histogram(heights)
            if area > answer:
                answer = area

        out.append(str(answer))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()