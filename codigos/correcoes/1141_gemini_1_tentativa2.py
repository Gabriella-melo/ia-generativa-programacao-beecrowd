import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    out = []
    
    while idx < len(input_data):
        N = int(input_data[idx])
        idx += 1
        
        if N == 0:
            break
            
        strings = input_data[idx : idx + N]
        idx += N
        
        # Ordena as strings pelo tamanho (crescente)
        strings.sort(key=len)
        
        # Mapeia cada string para seu índice na lista ordenada
        str_to_idx = {strings[i]: i for i in range(N)}
        
        # dp[i] armazena o tamanho da maior sequência terminando na string i
        dp = [1] * N
        max_ans = 1
        
        for i in range(N):
            s = strings[i]
            L = len(s)
            curr_dp = dp[i]
            
            if curr_dp > max_ans:
                max_ans = curr_dp
                
            # Procura por subpalavras de s com tamanho (L - 1)
            # que correspondem a transições válidas de tamanho exato +1
            seen = set()
            
            # Substring removendo o primeiro caractere
            sub1 = s[1:]
            seen.add(sub1)
            if sub1 in str_to_idx:
                j = str_to_idx[sub1]
                if dp[j] + 1 > curr_dp:
                    curr_dp = dp[j] + 1
                    
            # Substring removendo o último caractere
            sub2 = s[:-1]
            if sub2 not in seen:
                if sub2 in str_to_idx:
                    j = str_to_idx[sub2]
                    if dp[j] + 1 > curr_dp:
                        curr_dp = dp[j] + 1
                        
            # Para subcadeias menores, busca direta na lista de strings anteriores
            for j in range(i - 1, -1, -1):
                if dp[j] + 1 <= curr_dp:
                    continue
                if strings[j] in s:
                    curr_dp = dp[j] + 1
                    
            dp[i] = curr_dp
            if curr_dp > max_ans:
                max_ans = curr_dp
                
        out.append(str(max_ans))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()
