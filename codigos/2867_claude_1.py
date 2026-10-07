import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    c = int(data[idx]); idx += 1
    results = []
    for _ in range(c):
        n = int(data[idx]); idx += 1
        m = int(data[idx]); idx += 1
        value = n ** m
        results.append(str(len(str(value))))
    print("\n".join(results))

if __name__ == "__main__":
    main()