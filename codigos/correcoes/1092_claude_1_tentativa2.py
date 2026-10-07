import sys

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
                cnt = (r // 2) - ((l - 1) // 2)
                area = B[j] * cnt
                if area > max_area:
                    max_area = area
        stack.append(i)
    return max_area

def solve():
    data = sys.stdin.read().split()
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
                B = [0] * (2 * n - 1)
                B[0] = h_arr[0]
                for i in range(n - 1):
                    cap = h_arr[i] if h_arr[i] < h_arr[i + 1] else h_arr[i + 1]
                    left_val = a[i][j]
                    row_next = a[i + 1]
                    lo, hi, res = 1, cap, 0
                    while lo <= hi:
                        mid = (lo + hi) // 2
                        c1 = j - mid + 1
                        if left_val < row_next[c1]:
                            res = mid
                            lo = mid + 1
                        else:
                            hi = mid - 1
                    B[2 * i + 1] = res
                    B[2 * i + 2] = h_arr[i + 1]
            else:
                B = h_arr

            area = max_area_from_B(B)
            if area > best:
                best = area

        out.append(str(best))

    sys.stdout.write('\n'.join(out) + '\n')

solve()