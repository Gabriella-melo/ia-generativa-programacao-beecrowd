import sys
import math

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    C = int(input_data[0])
    idx = 1
    
    out = []
    for _ in range(C):
        n = int(input_data[idx])
        m = int(input_data[idx + 1])
        idx += 2
        
        if n == 0 or n == 1:
            out.append("1")
        else:
            num_digits = int(math.floor(m * math.log10(n))) + 1
            out.append(str(num_digits))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
