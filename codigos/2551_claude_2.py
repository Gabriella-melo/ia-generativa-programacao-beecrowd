import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    out = []
    n = len(data)
    while idx < n:
        N = int(data[idx]); idx += 1
        best = -1.0
        for day in range(1, N + 1):
            T = int(data[idx]); idx += 1
            D = int(data[idx]); idx += 1
            speed = D / T
            if speed > best:
                best = speed
                out.append(str(day))
    print('\n'.join(out))

if __name__ == "__main__":
    main()