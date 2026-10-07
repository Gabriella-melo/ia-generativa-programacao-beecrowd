import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    t = int(input_data[0])
    idx = 1
    out = []
    
    for _ in range(t):
        n = int(input_data[idx])
        m = int(input_data[idx + 1])
        idx += 2
        
        blocks = []
        for _ in range(n):
            blocks.append(int(input_data[idx]))
            idx += 1
            
        dp = [float('inf')] * (m + 1)
        dp[0] = 0
        
        for b in blocks:
            for j in range(b, m + 1):
                if dp[j - b] + 1 < dp[j]:
                    dp[j] = dp[j - b] + 1
                    
        out.append(str(dp[m]))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
