import sys

def main():
    lines = sys.stdin.read().split()
    if not lines:
        return
    
    idx = 0
    num_tokens = len(lines)
    
    while idx < num_tokens:
        N = int(lines[idx])
        idx += 1
        
        max_speed = -1.0
        
        for i in range(1, N + 1):
            T = int(lines[idx])
            D = int(lines[idx + 1])
            idx += 2
            
            speed = D / T
            if speed > max_speed:
                print(i)
                max_speed = speed

if __name__ == '__main__':
    main()
