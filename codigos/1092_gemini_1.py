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
            
        matrix = []
        for _ in range(N):
            row = [int(next(iterator)) for _ in range(M)]
            matrix.append(row)
            
        # R_valid[i][j] is the length of the strictly increasing sequence 
        # starting at (i, j) along the same row i.
        R_valid = [[1] * M for _ in range(N)]
        for i in range(N):
            for j in range(M - 2, -1, -1):
                if matrix[i][j] < matrix[i][j+1]:
                    R_valid[i][j] = R_valid[i][j+1] + 1

        # C_valid[i][j] is True if the transition from row i to row i+1 at position (i, j) is valid:
        # matrix[i][M-1] < matrix[i+1][0]
        C_valid = [[False] * M for _ in range(N)]
        for i in range(N - 1):
            if matrix[i][M - 1] < matrix[i + 1][0]:
                for j in range(M):
                    C_valid[i][j] = True

        max_area = 0

        for j in range(M):
            # Process column j across all rows i
            i = 0
            while i < N:
                start_i = i
                while i < N - 1 and C_valid[i][j] and R_valid[i][j] == M - j:
                    i += 1
                
                # Rows start_i to i can be stacked vertically except possibly 
                # the last row which might only have a partial width >= width needed.
                # Actually, all rows from start_i to i-1 MUST have full length (M - j)
                # to connect to the next row via C_valid.
                # The row i can have any length R_valid[i][j].
                
                # Segment length (number of full rows + 1)
                num_full_rows = i - start_i
                
                for k in range(1, M - j + 1):
                    # Height of submatrix with width k that can span full rows:
                    # If width k <= R_valid[i][j], the height is num_full_rows + 1.
                    # Otherwise, the height is num_full_rows.
                    if k <= R_valid[i][j]:
                        h = num_full_rows + 1
                    else:
                        h = num_full_rows
                    
                    area = h * k
                    if area > max_area:
                        max_area = area
                        
                i += 1

        print(max_area)

if __name__ == '__main__':
    solve()
