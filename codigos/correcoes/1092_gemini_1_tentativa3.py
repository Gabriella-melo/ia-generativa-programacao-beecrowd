import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    while True:
        try:
            N_str = next(iterator)
            M_str = next(iterator)
        except StopIteration:
            break
            
        N = int(N_str)
        M = int(M_str)
        
        if N == 0 and M == 0:
            break
            
        matrix = [[int(next(iterator)) for _ in range(M)] for _ in range(N)]
        
        # R_len[i][j]: length of strictly increasing sequence in row i starting at column j.
        # R_len[i][j] = R_len[i][j+1] + 1 if matrix[i][j] < matrix[i][j+1] else 1
        R_len = [[1] * M for _ in range(N)]
        for i in range(N):
            for j in range(M - 2, -1, -1):
                if matrix[i][j] < matrix[i][j+1]:
                    R_len[i][j] = R_len[i][j+1] + 1

        # C_valid[i]: True if the last element of row i is strictly less than the first element of row i+1
        C_valid = [False] * (N - 1)
        for i in range(N - 1):
            if matrix[i][M - 1] < matrix[i + 1][0]:
                C_valid[i] = True

        max_area = 1

        for j in range(M):
            # Find contiguous blocks of rows where C_valid is True
            r = 0
            while r < N:
                r_end = r
                while r_end < N - 1 and C_valid[r_end]:
                    r_end += 1
                
                # Rows from r to r_end (inclusive) can potentially be combined.
                # For row i in this block, the available width starting at column j is R_len[i][j].
                # However, for rows before the last row in a submatrix, their sequence MUST span
                # all the way to column M - 1 (i.e., R_len[i][j] must be M - j) to connect to the next row!
                
                # Find maximal subsegments [s, e] where all rows s..e-1 have R_len == M - j
                # and row e can have any R_len >= width.
                
                # Stack-based algorithm (largest rectangle in histogram) for rows r..r_end
                # Heights for histogram: for rows k in r..r_end-1, value is R_len[k][j] if R_len[k][j] == M - j else 0
                # But notice: if a row has R_len < M - j, it CANNOT be an internal row of the submatrix!
                # It can ONLY be the LAST row of the submatrix.
                
                # So we can split the block [r, r_end] at any row where R_len[k][j] < M - j.
                curr_start = r
                for k in range(r, r_end + 1):
                    # We can always form a submatrix of 1 row with width R_len[k][j]
                    if R_len[k][j] > max_area:
                        max_area = R_len[k][j]
                        
                    if k < r_end and R_len[k][j] < M - j:
                        # Row k cannot connect to row k+1 with full width M-j,
                        # but row k CAN act as the last row of a submatrix starting at curr_start!
                        h = k - curr_start + 1
                        w = R_len[k][j]
                        if h * w > max_area:
                            max_area = h * w
                        
                        # Full width submatrix up to row k-1
                        h_full = k - curr_start
                        w_full = M - j
                        if h_full * w_full > max_area:
                            max_area = h_full * w_full
                            
                        curr_start = k + 1
                
                # For the remaining segment from curr_start to r_end:
                # All rows from curr_start to r_end - 1 have R_len == M - j.
                # The last row r_end has R_len[r_end][j] (which could be anything <= M - j).
                num_full = r_end - curr_start
                if num_full > 0:
                    # Full width for all num_full rows
                    if num_full * (M - j) > max_area:
                        max_area = num_full * (M - j)
                    # Including last row r_end
                    last_w = R_len[r_end][j]
                    if (num_full + 1) * last_w > max_area:
                        max_area = (num_full + 1) * last_w
                
                r = r_end + 1

        print(max_area)

if __name__ == '__main__':
    solve()