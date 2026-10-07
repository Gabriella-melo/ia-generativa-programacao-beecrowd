import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    out = []
    while idx < len(data):
        n = int(data[idx]); idx += 1
        best = -1.0
        for day in range(1, n+1):
            t = int(data[idx]); idx += 1
            d = int(data[idx]); idx += 1
            speed = d / t
            if speed > best:
                best = speed
                out.append(str(day))
    print("\n".join(out))

if __name__ == "__main__":
    main()