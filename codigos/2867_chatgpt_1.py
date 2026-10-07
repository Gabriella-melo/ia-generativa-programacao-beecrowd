import sys
import math

def main():
    data = sys.stdin.read().split()
    c = int(data[0])
    pos = 1

    for _ in range(c):
        n = int(data[pos])
        m = int(data[pos + 1])
        pos += 2

        if n == 1:
            print(1)
        else:
            digits = int(m * math.log10(n)) + 1
            print(digits)

if __name__ == "__main__":
    main()