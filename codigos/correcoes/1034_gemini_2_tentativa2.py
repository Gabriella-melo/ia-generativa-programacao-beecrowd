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
        
        # Filtra blocos duplicados e maiores que M
        blocks = sorted(list(set(b for b in blocks if b <= m)))
        
        # Se M for divisível pelo maior bloco, o resultado é simples
        if m % blocks[-1] == 0:
            out.append(str(m // blocks[-1]))
            continue

        dp = [1000000000] * (m + 1)
        dp[0] = 0
        
        for b in blocks:
            for j in range(b, m + 1):
                cost = dp[j - b] + 1
                if cost < dp[j]:
                    dp[j] = cost
                    
        out.append(str(dp[m]))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()