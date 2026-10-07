import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    num_tokens = len(input_data)
    
    while idx < num_tokens:
        N = int(input_data[idx])
        idx += 1
        if N == 0:
            break
            
        strings = input_data[idx:idx+N]
        idx += N
        
        # Sort strings by length ascending
        strings.sort(key=len)
        
        # Mapping from string content to index in sorted array
        str_to_idx = {s: i for i, s in enumerate(strings)}
        
        dp = [1] * N
        max_seq = 0
        
        for i in range(N):
            s = strings[i]
            cur_dp = dp[i]
            if cur_dp > max_seq:
                max_seq = cur_dp
            
            n = len(s)
            
            # Check substrings obtained by removing the first character s[1:] 
            # or the last character s[:-1]
            if n > 1:
                sub1 = s[1:]
                sub2 = s[:-1]
                
                if sub1 in str_to_idx:
                    prev_idx = str_to_idx[sub1]
                    if dp[prev_idx] + 1 > cur_dp:
                        cur_dp = dp[prev_idx] + 1
                        
                if sub2 in str_to_idx:
                    prev_idx = str_to_idx[sub2]
                    if dp[prev_idx] + 1 > cur_dp:
                        cur_dp = dp[prev_idx] + 1
                        
                dp[i] = cur_dp
                if cur_dp > max_seq:
                    max_seq = cur_dp
                    
            # Propagate dp value to proper superstrings of s
            # s can transition to s + char or char + s
            for c in 'abcdefghijklmnopqrstuvwxyz':
                s1 = s + c
                if s1 in str_to_idx:
                    nxt = str_to_idx[s1]
                    if cur_dp + 1 > dp[nxt]:
                        dp[nxt] = cur_dp + 1
                
                s2 = c + s
                if s2 in str_to_idx:
                    nxt = str_to_idx[s2]
                    if cur_dp + 1 > dp[nxt]:
                        dp[nxt] = cur_dp + 1
                        
        print(max_seq)

if __name__ == '__main__':
    solve()