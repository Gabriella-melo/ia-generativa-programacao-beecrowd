def main():
    import sys
    data = sys.stdin.read().split()
    idx = 0
    p = int(data[idx]); idx += 1
    n = int(data[idx]); idx += 1
    heights = [int(data[idx + i]) for i in range(n)]
    ok = True
    for i in range(1, n):
        if abs(heights[i] - heights[i-1]) > p:
            ok = False
            break
    print("YOU WIN" if ok else "GAME OVER")

main()