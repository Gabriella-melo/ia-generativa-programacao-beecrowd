import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    out = []

    while True:
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        if n == 0 and m == 0:
            break

        arr = []
        for i in range(n):
            row = data[idx:idx + m]
            idx += m
            arr.append([int(x) for x in row])

        # L[i][j] = length of the increasing run ending at column j in row i
        L = [[1] * m for _ in range(n)]
        for i in range(n):
            ai = arr[i]
            Li = L[i]
            for j in range(1, m):
                if ai[j] > ai[j - 1]:
                    Li[j] = Li[j - 1] + 1
                else:
                    Li[j] = 1

        best = 1

        for w in range(m, 0, -1):
            if w * n <= best:
                break

            K = m - w + 1
            target = w * n

            for c1 in range(K):
                c2 = c1 + w - 1
                run = 0
                prev_ok = False
                maxrun = 0

                for i in range(n):
                    if L[i][c2] >= w:
                        if prev_ok and arr[i - 1][c2] < arr[i][c1]:
                            run += 1
                        else:
                            run = 1
                        prev_ok = True
                        if run > maxrun:
                            maxrun = run
                    else:
                        run = 0
                        prev_ok = False

                candidate = maxrun * w
                if candidate > best:
                    best = candidate
                    if best == target:
                        break

        out.append(str(best))

    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))


if __name__ == "__main__":
    main()