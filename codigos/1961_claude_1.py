def main():
    import sys
    data = sys.stdin.read().split()
    idx = 0
    p = int(data[idx]); idx += 1
    n = int(data[idx]); idx += 1
    heights = [int(data[idx+i]) for i in range(n)]
    can_win = True
    for i in range(1, n):
        if abs(heights[i] - heights[i-1]) > p:
            can_win = False
            break
    print("YOU WIN" if can_win else "GAME OVER")

main()