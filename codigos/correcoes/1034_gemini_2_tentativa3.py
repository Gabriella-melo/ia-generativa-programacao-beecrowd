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
        
        blocks = [int(x) for x in input_data[idx:idx + n]]
        idx += n
        
        blocks = sorted(list(set(b for b in blocks if b <= m)))
        
        INF = 1000000000
        dp = [INF] * (m + 1)
        dp[0] = 0
        
        for i in range(1, m + 1):
            min_val = INF
            for b in blocks:
                if b > i:
                    break
                val = dp[i - b]
                if val < min_val:
                    min_val = val
            dp[i] = min_val + 1
            
        out.append(str(dp[m]))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()