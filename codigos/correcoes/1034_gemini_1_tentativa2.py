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
        
        blocks = [int(x) for x in input_data[idx:idx+N]]
        idx += N
        
        # Filtra blocos únicos para evitar redundância
        blocks = list(set(blocks))
        
        # Estrutura para BFS / Unbounded Knapsack otimizada
        dist = [-1] * (M + 1)
        dist[0] = 0
        queue = [0]
        
        found = False
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            d = dist[u]
            
            for b in blocks:
                nxt = u + b
                if nxt == M:
                    out.append(str(d + 1))
                    found = True
                    break
                if nxt < M and dist[nxt] == -1:
                    dist[nxt] = d + 1
                    queue.append(nxt)
            if found:
                break

    print('\n'.join(out))

if __name__ == '__main__':
    solve()