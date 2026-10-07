import sys
from bisect import bisect_right

def max_area_from_B(B):
    L = len(B)
    stack = []
    max_area = 0
    for i in range(L + 1):
        curH = B[i] if i < L else -1
        while stack and B[stack[-1]] >= curH:
            j = stack.pop()
            left = stack[-1] if stack else -1
            l = left + 1
            r = i - 1
            if l <= r:
                cnt = (r >> 1) - ((l - 1) >> 1)
                area = B[j] * cnt
                if area > max_area:
                    max_area = area
        stack.append(i)
    return max_area

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    out = []
    while True:
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        if n == 0 and m == 0:
            break

        a = []
        for i in range(n):
            row = data[idx: idx + m]
            idx += m
            a.append([int(x) for x in row])

        # runlen[i][j] = length of maximal strictly increasing run ending at (i,j)
        runlen = [[1] * m for _ in range(n)]
        for i in range(n):
            ai = a[i]
            ri = runlen[i]
            for j in range(1, m):
                if ai[j - 1] < ai[j]:
                    ri[j] = ri[j - 1] + 1
                else:
                    ri[j] = 1

        best = 1

        for j in range(m):
            h_arr = [runlen[i][j] for i in range(n)]

            if n > 1:
                size = 2 * n - 1
                B = [0] * size
                B[0] = h_arr[0]
                for i in range(n - 1):
                    hi_i = h_arr[i]
                    hi_i1 = h_arr[i + 1]
                    cap = hi_i if hi_i < hi_i1 else hi_i1
                    c1_min = j - cap + 1
                    val = a[i][j]
                    row_next = a[i + 1]
                    pos = bisect_right(row_next, val, c1_min, j + 1)
                    w = j - pos + 1
                    B[2 * i + 1] = w
                    B[2 * i + 2] = hi_i1
            else:
                B = h_arr

            area = max_area_from_B(B)
            if area > best:
                best = area

        out.append(str(best))

    sys.stdout.write('\n'.join(out) + '\n')

solve()