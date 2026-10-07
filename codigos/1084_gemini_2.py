import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    output = []
    
    while idx < len(input_data):
        n = int(input_data[idx])
        d = int(input_data[idx+1])
        idx += 2
        
        if n == 0 and d == 0:
            break
            
        s = input_data[idx]
        idx += 1
        
        keep = n - d
        stack = []
        to_remove = d
        
        for digit in s:
            while stack and to_remove > 0 and stack[-1] < digit:
                stack.pop()
                to_remove -= 1
            stack.append(digit)
            
        output.append("".join(stack[:keep]))
        
    print("\n".join(output))

if __name__ == '__main__':
    main()
