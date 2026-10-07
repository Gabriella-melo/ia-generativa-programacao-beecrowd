import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    p = int(input_data[0])
    n = int(input_data[1])
    heights = [int(x) for x in input_data[2:2+n]]
    
    for i in range(n - 1):
        if abs(heights[i+1] - heights[i]) > p:
            print("GAME OVER")
            return
            
    print("YOU WIN")

if __name__ == '__main__':
    main()
