import sys
import numpy as np

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
        cnt_vals = n * m
        flat = data[idx: idx + cnt_vals]
        idx += cnt_vals
        a = np.array(flat, dtype=np.int64).reshape(n, m)

        runlen = np.ones((n, m), dtype=np.int64)
        for j in range(1, m):
            inc = a[:, j - 1] < a[:, j]
            runlen[:, j] = np.where(inc, runlen[:, j - 1] + 1, 1)

        best = 0

        if n > 1:
            a_next = a[1:, :]  # rows 1..n-1

        idx_range = np.arange(n - 1) if n > 1 else None

        for c2 in range(m):
            h_arr = runlen[:, c2]
            if n > 1:
                cap = np.minimum(h_arr[:-1], h_arr[1:]).astype(np.int64)
                lo = np.ones(n - 1, dtype=np.int64)
                hi = cap.copy()
                res = np.zeros(n - 1, dtype=np.int64)
                left_val = a[:-1, c2]
                active = lo <= hi
                while np.any(active):
                    mid = (lo + hi) // 2
                    c1 = c2 - mid + 1
                    vals = a_next[idx_range, c1]
                    cond = left_val < vals
                    upd = active & cond
                    res = np.where(upd, mid, res)
                    lo = np.where(upd, mid + 1, lo)
                    hi = np.where(active & (~cond), mid - 1, hi)
                    active = lo <= hi
                edgeThreshold = res
                B = np.empty(2 * n - 1, dtype=np.int64)
                B[0::2] = h_arr
                B[1::2] = edgeThreshold
            else:
                B = h_arr.copy()

            Bl = B.tolist()
            area = max_area_from_B(Bl)
            if area > best:
                best = area

        out.append(str(best))

    sys.stdout.write('\n'.join(out) + '\n')

solve()