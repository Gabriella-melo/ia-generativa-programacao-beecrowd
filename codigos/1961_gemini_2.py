import sys

def main():
    lines = sys.stdin.read().split()
    if not lines:
        return
    
    p = int(lines[0])
    n = int(lines[1])
    
    heights = [int(x) for x in lines[2:2+n]]
    
    for i in range(n - 1):
        if abs(heights[i+1] - heights[i]) > p:
            print("GAME OVER")
            return
            
    print("YOU WIN")

if __name__ == '__main__':
    main()
