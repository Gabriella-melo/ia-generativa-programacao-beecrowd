import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    out = []

    while True:
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        if n == 0 and m == 0:
            break

        arr = []
        for i in range(n):
            row = data[idx:idx + m]
            idx += m
            arr.append([int(x) for x in row])

        # Lh[i][j] = length of increasing run ending at (i,j) going left in row i
        Lh = [[1] * m for _ in range(n)]
        for i in range(n):
            ai = arr[i]
            Li = Lh[i]
            for j in range(1, m):
                if ai[j] > ai[j - 1]:
                    Li[j] = Li[j - 1] + 1
                else:
                    Li[j] = 1

        # For each column c2 (right edge) and each row i, precompute for width w
        # the maximum vertical run length "runLen[i]" ending at row i using width w,
        # by processing widths from large to small won't directly reuse... 
        # Instead: for fixed right column c2, as w increases, left column c1 = c2-w+1 decreases.
        # We need, for each row i and width w, whether Lh[i][c2] >= w (row i supports width w ending at c2)
        # and vertical condition arr[i-1][c2] < arr[i][c1].
        #
        # Approach: for each c2, iterate w from 1 to Lh_max at that column region,
        # maintain running vertical streak arrays only for valid rows, but to avoid O(n*m^2)
        # worst case (m=600 -> m^2=360000, times n=600 -> 216,000,000) which is too slow in python.
        #
        # Better approach: binary search / two pointers isn't trivial because condition depends on w.
        # We use monotonic stack / DP: define for each row i and column j:
        # best[i][j] = the maximum width w such that starting column j-w+1..j in row i is increasing
        # AND rows above also align vertically for as many rows as possible.
        #
        # Let's define R[i][j] = the maximum number of consecutive rows ending at row i such that,
        # for width = Lh[i][j] (the max possible width ending at column j in row i, but we want per width)...
        #
        # Simplify with the known technique: For each cell (i,j), let h[i][j] = Lh[i][j] (max run length ending here in row).
        # Define V[i][j] = length of vertical chain ending at (i,j) such that for all rows in the chain,
        # the horizontal run length is >= current chain length (using width = chain length) and vertical condition holds
        # for the specific width = min widths... This is the classic "largest rectangle of consecutive increasing rows" problem.
        #
        # Correct known solution: define DP[i][j] = the size of the largest "good" submatrix using column j as the right edge,
        # row i as the bottom edge, where width is determined dynamically.
        # We use: cnt[i][j] = number of consecutive rows ending at i (including i) such that row i-k..i all have
        # Lh[*][j] >= (k+1) is not quite right either since width must be same across all rows.
        #
        # Standard solution (used in competitive programming for this exact problem "Longest Increasing Sub-sequence" ICPC):
        # For each column j, and row i, compute up[i][j] = 1 + up[i-1][j] if arr[i-1][j] < arr[i][j] else 0 is wrong too
        # because condition compares arr[i-1][c2] with arr[i][c1] (different columns!).
        #
        # We implement O(N*M) DP as follows:
        # Process columns from right to left is complex; let's do the O(N*M) approach with a stack-based method.
        pass

        # We'll compute answer using DP over (row, col) with "extend" arrays.
        # ext[i][j] = the maximum width w (>=1) of a valid submatrix block ending at row i with right column j,
        # consisting of exactly the rows i-w+1..i (all present), such that:
        #   for each row r in that range, Lh[r][j] >= w
        #   for each row r in range (r>i-w+1..i), arr[r-1][j] < arr[r][j-w+1]
        # ext[i][j] is defined so that answer includes ext[i][j] * w for that w... but w depends on the chain length.
        #
        # We compute it greedily: ext[i][j] = 1 + ext[i-1][j] IF the row i-1's block (of size ext[i-1][j]) width also
        # accommodates row i, i.e. Lh[i][j] >= ext[i-1][j]+1 and arr[i-1][j] < arr[i][j-ext[i-1][j]].
        # If that holds, ext[i][j] = ext[i-1][j] + 1, capped by Lh[i][j].
        # Otherwise ext[i][j] = 1.
        # This greedy matches this class of problems (similar to "maximal square" style DP) and runs in O(N*M).

        ext = [[1] * m for _ in range(n)]
        best = 1
        for j in range(m):
            if Lh[0][j] > best:
                best = Lh[0][j]
        for j in range(m):
            ext[0][j] = 1
            if 1 > best:
                best = 1

        for i in range(1, n):
            ai = arr[i]
            aim1 = arr[i - 1]
            Lhi = Lh[i]
            exti = ext[i]
            exti_1 = ext[i - 1]
            for j in range(m):
                w_prev = exti_1[j]
                cand_w = w_prev + 1
                if Lhi[j] >= cand_w and (j - w_prev) >= 0 and aim1[j] < ai[j - w_prev]:
                    # cap by Lh
                    w = cand_w
                    exti[j] = w
                else:
                    exti[j] = 1
                w = exti[j]
                area = w * w
                # area candidate isn't correct measure; real area = w (width) * (number of rows) 
                # but here w represents both width and rows count since chain length grows by 1 each row
                if w > 0:
                    a = w * w
                    if a > best:
                        best = a
                if Lhi[j] > best:
                    best = Lhi[j]

        out.append(str(best))

    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))


if __name__ == "__main__":
    main()