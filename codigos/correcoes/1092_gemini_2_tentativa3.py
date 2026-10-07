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
        
        valid_len = [[1] * M for _ in range(N)]
        for i in range(N):
            row = matrix[i]
            v_row = valid_len[i]
            for j in range(M - 2, -1, -1):
                if row[j] < row[j+1]:
                    v_row[j] = v_row[j+1] + 1
        
        link = [False] * (N - 1)
        for i in range(N - 1):
            if matrix[i][M-1] < matrix[i+1][0]:
                link[i] = True
        
        ans = 0
        
        for c in range(M):
            r = 0
            while r < N:
                start_r = r
                chain = [valid_len[r][c]]
                while r < N - 1 and link[r]:
                    r += 1
                    chain.append(valid_len[r][c])
                r += 1
                
                k = len(chain)
                left = [-1] * k
                right = [k] * k
                
                stack = []
                for i in range(k):
                    val = chain[i]
                    while stack and chain[stack[-1]] >= val:
                        stack.pop()
                    if stack:
                        left[i] = stack[-1]
                    stack.append(i)
                
                stack = []
                for i in range(k - 1, -1, -1):
                    val = chain[i]
                    while stack and chain[stack[-1]] >= val:
                        stack.pop()
                    if stack:
                        right[i] = stack[-1]
                    stack.append(i)
                
                for i in range(k):
                    height = right[i] - left[i] - 1
                    size = height * chain[i]
                    if size > ans:
                        ans = size
                        
        out.append(str(ans))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()