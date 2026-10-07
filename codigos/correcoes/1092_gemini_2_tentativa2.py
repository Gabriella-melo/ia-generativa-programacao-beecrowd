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
        
        # Precomputa o tamanho do segmento estritamente crescente na mesma linha.
        valid_len = [[1] * M for _ in range(N)]
        for i in range(N):
            for j in range(M - 2, -1, -1):
                if matrix[i][j] < matrix[i][j+1]:
                    valid_len[i][j] = valid_len[i][j+1] + 1
        
        # link[i] indica se a transição entre o fim da linha i e o início da linha i+1 é crescente.
        link = [False] * (N - 1)
        for i in range(N - 1):
            if matrix[i][M-1] < matrix[i+1][0]:
                link[i] = True
        
        max_submatrix_size = 0
        
        # Para cada coluna inicial, encontramos as cadeias verticais de linhas válidas
        for c in range(M):
            r = 0
            while r < N:
                # Se a linha atual nem possui o tamanho mínimo de submatriz já encontrado, podemos pular
                w_current = valid_len[r][c]
                
                # Encontra o bloco contínuo de linhas que podem se conectar
                start_r = r
                min_w = w_current
                
                while r < N:
                    min_w = min(min_w, valid_len[r][c])
                    height = r - start_r + 1
                    
                    # Se o comprimento máximo de linha for 0 ou se quebrar a transição
                    if min_w == 0:
                        break
                        
                    size = height * min_w
                    if size > max_submatrix_size:
                        max_submatrix_size = size
                        
                    if r < N - 1 and link[r]:
                        r += 1
                    else:
                        break
                r += 1

        # Otimização principal: iterar a partir das colunas em ordem e limitar por W
        # Re-calcula de forma direta usando PD por coluna inicial
        ans = 0
        for c in range(M):
            # Cadeias de linhas consecutivas com link[i] == True
            chains = []
            curr_chain = []
            for i in range(N):
                curr_chain.append(valid_len[i][c])
                if i < N - 1 and not link[i]:
                    chains.append(curr_chain)
                    curr_chain = []
            if curr_chain:
                chains.append(curr_chain)
                
            for chain in chains:
                k = len(chain)
                # Para cada sub-cadeia, o tamanho máximo é a altura * largura_minima
                for i in range(k):
                    min_w = chain[i]
                    for j in range(i, k):
                        if chain[j] < min_w:
                            min_w = chain[j]
                        size = (j - i + 1) * min_w
                        if size > ans:
                            ans = size
                            
        out.append(str(ans))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()