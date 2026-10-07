import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    Xm, Ym, Xr, Yr = map(int, input_data)
    distance = abs(Xm - Xr) + abs(Ym - Yr)
    print(distance)

if __name__ == '__main__':
    main()
