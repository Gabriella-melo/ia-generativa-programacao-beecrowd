import sys

def main():
    lines = sys.stdin.read().split()
    if not lines:
        return
    
    idx = 0
    n_lines = len(lines)
    
    while idx < n_lines:
        n = int(lines[idx])
        idx += 1
        
        max_speed = -1.0
        
        for day in range(1, n + 1):
            t = int(lines[idx])
            d = int(lines[idx + 1])
            idx += 2
            
            speed = d / t
            if speed > max_speed:
                max_speed = speed
                print(day)

if __name__ == '__main__':
    main()
