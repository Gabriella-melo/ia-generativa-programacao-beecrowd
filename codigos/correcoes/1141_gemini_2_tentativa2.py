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
        
        # Map each string to its maximum sequence length ending at this string
        dp = {}
        max_seq = 0
        
        for s in strings:
            cur_max = 0
            n = len(s)
            
            # Check substrings of length n-1 (removing first or last character)
            if n > 1:
                sub1 = s[1:]
                sub2 = s[:-1]
                if sub1 in dp and dp[sub1] > cur_max:
                    cur_max = dp[sub1]
                if sub2 in dp and dp[sub2] > cur_max:
                    cur_max = dp[sub2]
            
            val = cur_max + 1
            dp[s] = val
            if val > max_seq:
                max_seq = val
                
        print(max_seq)

if __name__ == '__main__':
    solve()