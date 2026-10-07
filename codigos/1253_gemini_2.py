import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    N = int(input_data[0].strip())
    line_idx = 1
    
    for _ in range(N):
        if line_idx >= len(input_data):
            break
        text = input_data[line_idx].strip()
        line_idx += 1
        
        if line_idx >= len(input_data):
            break
        shift = int(input_data[line_idx].strip())
        line_idx += 1
        
        decoded = []
        for char in text:
            if 'A' <= char <= 'Z':
                # To decode a right shift, we shift left by 'shift'
                decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                decoded.append(decoded_char)
            else:
                decoded.append(char)
                
        print("".join(decoded))

if __name__ == '__main__':
    solve()
