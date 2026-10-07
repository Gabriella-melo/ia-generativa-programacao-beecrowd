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
        
        dp = [1] * N
        max_len = 0
        
        for i in range(N):
            curr_str = strings[i]
            curr_dp = dp[i]
            if curr_dp > max_len:
                max_len = curr_dp
                
            length_i = len(curr_str)
            
            # Optimization: Pre-generate unique target indices using string matching
            # Since sum of lengths <= 10^6, we look ahead to strings that contain `curr_str`
            for j in range(i + 1, N):
                next_str = strings[j]
                if len(next_str) == length_i:
                    continue
                if dp[j] < curr_dp + 1:
                    if curr_str in next_str:
                        dp[j] = curr_dp + 1
                        
        print(max_len)

if __name__ == '__main__':
    solve()
