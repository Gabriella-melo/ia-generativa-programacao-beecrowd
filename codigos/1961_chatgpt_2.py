P, N = map(int, input().split())
pipes = list(map(int, input().split()))

for i in range(N - 1):
    if abs(pipes[i] - pipes[i + 1]) > P:
        print("GAME OVER")
        break
else:
    print("YOU WIN")