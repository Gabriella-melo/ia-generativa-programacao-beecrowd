import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    T = int(input_data[0])
    idx = 1
    out = []
    
    for _ in range(T):
        N = int(input_data[idx])
        M = int(input_data[idx+1])
        idx += 2
        
        blocks = set()
        for i in range(N):
            blocks.add(int(input_data[idx + i]))
        idx += N
        
        blocks = sorted(list(blocks), reverse=True)
        
        INF = float('inf')
        dp = [INF] * (M + 1)
        dp[0] = 0
        
        for b in blocks:
            for j in range(b, M + 1):
                if dp[j - b] + 1 < dp[j]:
                    dp[j] = dp[j - b] + 1
                    
        out.append(str(dp[M]))

    print('\n'.join(out))

if __name__ == '__main__':
    solve()