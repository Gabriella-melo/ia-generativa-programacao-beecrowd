import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    out = []
    
    while idx < len(input_data):
        N = int(input_data[idx])
        D = int(input_data[idx + 1])
        idx += 2
        
        if N == 0 and D == 0:
            break
            
        digits = input_data[idx]
        idx += 1
        
        to_remove = D
        stack = []
        
        for digit in digits:
            while stack and to_remove > 0 and stack[-1] < digit:
                stack.pop()
                to_remove -= 1
            stack.append(digit)
            
        target_len = N - D
        out.append("".join(stack[:target_len]))
        
    print("\n".join(out))

if __name__ == '__main__':
    solve()
