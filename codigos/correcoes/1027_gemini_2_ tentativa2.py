import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    while True:
        try:
            n_str = next(iterator)
        except StopIteration:
            break
        
        N = int(n_str)
        
        # Guardar pontos agrupados por Y para encontrar candidatos a (Y, Y+2) com base nos dados reais
        points_by_y = {}
        for _ in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            if y not in points_by_y:
                points_by_y[y] = []
            points_by_y[y].append(x)
        
        # Considerar apenas pares de Y onde ao menos um ponto existe
        candidate_bases = set()
        for y in points_by_y:
            candidate_bases.add(y)
            candidate_bases.add(y - 2)
            
        max_overall = 0
        
        for y_low in candidate_bases:
            y_high = y_low + 2
            
            pts_low = points_by_y.get(y_low, [])
            pts_high = points_by_y.get(y_high, [])
            
            if not pts_low and not pts_high:
                continue
            
            # Ordenar e mesclar os pontos com X para simular a passagem de forma eficiente
            # Usando dois ponteiros nos vetores ordenados de X para y_low e y_high
            pts_low_sorted = sorted(pts_low)
            pts_high_sorted = sorted(pts_high)
            
            i, j = 0, 0
            len_low, len_high = len(pts_low_sorted), len(pts_high_sorted)
            
            dp0 = 0  # Max sequência alternada terminando em y_low
            dp1 = 0  # Max sequência alternada terminando em y_high
            
            while i < len_low or j < len_high:
                if i < len_low and j < len_high:
                    x_low = pts_low_sorted[i]
                    x_high = pts_high_sorted[j]
                    
                    if x_low < x_high:
                        has_low, has_high = True, False
                        x_curr = x_low
                    elif x_high < x_low:
                        has_low, has_high = False, True
                        x_curr = x_high
                    else:
                        has_low, has_high = True, True
                        x_curr = x_low
                elif i < len_low:
                    has_low, has_high = True, False
                    x_curr = pts_low_sorted[i]
                else:
                    has_low, has_high = False, True
                    x_curr = pts_high_sorted[j]
                
                # Avançar ponteiros que possuem o mesmo X atual
                if has_low:
                    while i < len_low and pts_low_sorted[i] == x_curr:
                        i += 1
                if has_high:
                    while j < len_high and pts_high_sorted[j] == x_curr:
                        j += 1
                
                # Atualização do DP para a posição X atual
                next_dp0 = max(dp0, dp1 + 1) if has_low else dp0
                next_dp1 = max(dp1, dp0 + 1) if has_high else dp1
                
                dp0, dp1 = next_dp0, next_dp1
            
            if dp0 > max_overall:
                max_overall = dp0
            if dp1 > max_overall:
                max_overall = dp1
                
        print(max_overall)

if __name__ == '__main__':
    solve()