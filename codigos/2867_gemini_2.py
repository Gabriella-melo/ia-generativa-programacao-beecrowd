import sys
import math

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    C = int(input_data[0])
    idx = 1
    
    for _ in range(C):
        if idx >= len(input_data):
            break
        N = int(input_data[idx])
        M = int(input_data[idx+1])
        idx += 2
        
        if N == 0:
            print(1)
        elif N == 1:
            print(1)
        else:
            digits = int(M * math.log10(N)) + 1
            print(digits)

if __name__ == '__main__':
    main()
