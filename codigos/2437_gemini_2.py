import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    Xm, Ym, Xr, Yr = map(int, input_data)
    print(abs(Xm - Xr) + abs(Ym - Yr))

if __name__ == '__main__':
    main()
