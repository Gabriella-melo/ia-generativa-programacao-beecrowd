import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline
    output = []

    while True:
        line = input()
        if not line:
            break

        n, m = map(int, line.split())
        if n == 0 and m == 0:
            break

        a = [list(map(int, input().split())) for _ in range(n)]

        # inc[i][j] = maximum width of a strictly increasing
        # sequence beginning at (i, j).
        inc = [[1] * m for _ in range(n)]

        for i in range(n):
            row = a[i]
            dp = inc[i]
            for j in range(m - 2, -1, -1):
                if row[j] < row[j + 1]:
                    dp[j] = dp[j + 1] + 1

        answer = 1

        for left in range(m):
            # Capacities are stored in an alternating sequence:
            #
            # V0, E0, V1, E1, ..., E(n-2), V(n-1)
            #
            # Vi = maximum width allowed by row i.
            # Ei = maximum width for which the transition from
            #      row i to row i+1 is strictly increasing.
            #
            # For any rectangle, its width is the minimum capacity
            # among the vertices and edges it contains.
            length = 2 * n - 1
            cap = [0] * length

            for i in range(n):
                cap[2 * i] = inc[i][left]

            for i in range(n - 1):
                limit = inc[i][left]
                target = a[i + 1][left]

                # a[i][left:left+limit] is strictly increasing,
                # so the first value >= target determines the
                # maximum possible width across this boundary.
                pos = bisect_left(a[i], target, left, left + limit)
                cap[2 * i + 1] = pos - left

            # For every capacity, find the largest interval in which
            # it is a minimum. Use previous strictly smaller and
            # next smaller-or-equal boundaries.
            #
            # Only even positions represent rows. The number of
            # even positions in [l, r] is the number of rows covered.
            left_bound = [-1] * length
            stack = []

            for p in range(length):
                while stack and cap[stack[-1]] >= cap[p]:
                    stack.pop()
                left_bound[p] = stack[-1] if stack else -1
                stack.append(p)

            right_bound = [length] * length
            stack.clear()

            for p in range(length - 1, -1, -1):
                while stack and cap[stack[-1]] > cap[p]:
                    stack.pop()
                right_bound[p] = stack[-1] if stack else length
                stack.append(p)

            for p in range(length):
                c = cap[p]
                if c <= 0:
                    continue

                l = left_bound[p] + 1
                r = right_bound[p] - 1

                # First and last even positions in [l, r].
                first_row = (l + 1) // 2
                last_row = (r // 2)

                if first_row <= last_row:
                    rows = last_row - first_row + 1
                    area = c * rows
                    if area > answer:
                        answer = area

        output.append(str(answer))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()