import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    out = []
    
    while idx < len(input_data):
        N_str = input_data[idx]
        idx += 1
        
        N = int(N_str)
        if N == 0:
            break
            
        strings = input_data[idx : idx + N]
        idx += N
        
        strings.sort(key=len)
        
        dp = [1] * N
        str_to_idx = {strings[i]: i for i in range(N)}
        
        max_ans = 1 if N > 0 else 0
        
        for i in range(N):
            s = strings[i]
            L = len(s)
            curr_dp = dp[i]
            if curr_dp > max_ans:
                max_ans = curr_dp
                
            seen_neighbors = set()
            
            if L > 1:
                sub1 = s[1:]
                seen_neighbors.add(sub1)
                if sub1 in str_to_idx:
                    j = str_to_idx[sub1]
                    if curr_dp + 1 > dp[j]:
                        dp[j] = curr_dp + 1
                        
                sub2 = s[:-1]
                if sub2 not in seen_neighbors:
                    seen_neighbors.add(sub2)
                    if sub2 in str_to_idx:
                        j = str_to_idx[sub2]
                        if curr_dp + 1 > dp[j]:
                            dp[j] = curr_dp + 1
            
            for k in range(N - 1, i, -1):
                if dp[k] + (k - i) <= max_ans:
                    break
                if dp[k] < curr_dp + 1:
                    if s in strings[k]:
                        dp[k] = curr_dp + 1
                        if curr_dp + 1 > max_ans:
                            max_ans = curr_dp + 1
                            
        out.append(str(max_ans))
        
    print('\n'.join(out))

if __name__ == '__main__':
    main()
