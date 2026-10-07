import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    while True:
        try:
            N = int(next(iterator))
            M = int(next(iterator))
        except StopIteration:
            break
            
        if N == 0 and M == 0:
            break
            
        matrix = [[int(next(iterator)) for _ in range(M)] for _ in range(N)]
            
        R_valid = [[1] * M for _ in range(N)]
        for i in range(N):
            for j in range(M - 2, -1, -1):
                if matrix[i][j] < matrix[i][j+1]:
                    R_valid[i][j] = R_valid[i][j+1] + 1

        C_valid = [False] * (N - 1)
        for i in range(N - 1):
            if matrix[i][M - 1] < matrix[i + 1][0]:
                C_valid[i] = True

        max_area = 1

        for j in range(M):
            max_possible_width = M - j
            i = 0
            while i < N:
                start_i = i
                while i < N - 1 and C_valid[i] and R_valid[i][j] == max_possible_width:
                    i += 1
                
                num_full_rows = i - start_i
                last_row_len = R_valid[i][j]
                
                area1 = (num_full_rows + 1) * last_row_len
                area2 = num_full_rows * max_possible_width
                
                if area1 > max_area:
                    max_area = area1
                if area2 > max_area:
                    max_area = area2
                        
                i += 1

        print(max_area)

if __name__ == '__main__':
    solve()