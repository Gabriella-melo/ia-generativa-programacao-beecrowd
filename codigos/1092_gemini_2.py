import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    out = []
    
    while idx < len(input_data):
        N = int(input_data[idx])
        M = int(input_data[idx+1])
        idx += 2
        
        if N == 0 and M == 0:
            break
        
        matrix = []
        for _ in range(N):
            matrix.append([int(x) for x in input_data[idx:idx+M]])
            idx += M
        
        # valid_len[i][j] stores the length of the strictly increasing 
        # sequence starting at (i, j) along the linearized matrix, 
        # considering only elements in the same row i.
        valid_len = [[1] * M for _ in range(N)]
        for i in range(N):
            for j in range(M - 2, -1, -1):
                if matrix[i][j] < matrix[i][j+1]:
                    valid_len[i][j] = valid_len[i][j+1] + 1
        
        # link[i] is True if matrix[i][M-1] < matrix[i+1][0]
        link = [False] * (N - 1)
        for i in range(N - 1):
            if matrix[i][M-1] < matrix[i+1][0]:
                link[i] = True
        
        max_submatrix_size = 0
        
        # For each possible column width W from 1 to M
        for W in range(1, M + 1):
            if W * N <= max_submatrix_size:
                continue
                
            c = 0
            while c <= M - W:
                # Find maximal contiguous blocks of rows starting at column c
                # where row i can transition to row i+1.
                r = 0
                while r < N:
                    # Check if row r has an increasing segment of length W starting at c
                    if valid_len[r][c] < W:
                        r += 1
                        continue
                    
                    # Row r is valid. Find how far down we can extend this block.
                    start_r = r
                    while r < N - 1 and link[r] and valid_len[r+1][c] >= W:
                        r += 1
                    
                    height = r - start_r + 1
                    size = height * W
                    if size > max_submatrix_size:
                        max_submatrix_size = size
                    
                    r += 1
                c += 1
                
        out.append(str(max_submatrix_size))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
