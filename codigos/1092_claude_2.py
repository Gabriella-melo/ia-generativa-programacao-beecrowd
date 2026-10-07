import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    out_lines = []
    L_data = data
    while pos < len(data):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        if n == 0 and m == 0:
            break
        total = n * m
        vals = data[pos:pos + total]
        pos += total
        arr = np.empty(total, dtype=np.int64)
        for i in range(total):
            arr[i] = int(vals[i])
        arr = arr.reshape(n, m)

        L = np.ones((n, m), dtype=np.int64)
        for j in range(1, m):
            greater = arr[:, j] > arr[:, j - 1]
            L[:, j] = np.where(greater, L[:, j - 1] + 1, 1)

        best = 1
        idx_col = np.arange(n, dtype=np.int64).reshape(-1, 1)

        for w in range(1, m + 1):
            K = m - w + 1
            c1 = np.arange(K)
            c2 = c1 + w - 1

            Valid = L[:, c2] >= w  # shape (n, K)

            can_continue = np.zeros((n, K), dtype=bool)
            if n > 1:
                Boundary = arr[:-1, c2] < arr[1:, c1]
                can_continue[1:, :] = Valid[1:, :] & Valid[:-1, :] & Boundary

            marker = np.where(~can_continue, idx_col, -1)
            run_start_before = np.maximum.accumulate(marker, axis=0)
            streak = (idx_col - run_start_before + 1) * Valid

            max_streak = int(streak.max())
            candidate = max_streak * w
            if candidate > best:
                best = candidate

        out_lines.append(str(best))

    sys.stdout.write('\n'.join(out_lines) + ('\n' if out_lines else ''))


if __name__ == "__main__":
    main()