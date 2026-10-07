import sys
from collections import defaultdict

def solve_case(points):
    by_y = defaultdict(list)

    for x, y in points:
        by_y[y].append(x)

    for y in by_y:
        by_y[y].sort()

    best = 0

    for low in by_y:
        high = low + 2

        if high not in by_y:
            continue

        low_x = by_y[low]
        high_x = by_y[high]

        i = j = 0
        dp_low = dp_high = 0

        while i < len(low_x) or j < len(high_x):
            if j == len(high_x) or (i < len(low_x) and low_x[i] < high_x[j]):
                x = low_x[i]
                i += 1

                while i < len(low_x) and low_x[i] == x:
                    i += 1

                new_low = max(dp_low, dp_high + 1 if dp_high else 1)
                dp_low = new_low

            elif i == len(low_x) or high_x[j] < low_x[i]:
                x = high_x[j]
                j += 1

                while j < len(high_x) and high_x[j] == x:
                    j += 1

                new_high = max(dp_high, dp_low + 1 if dp_low else 1)
                dp_high = new_high

            else:
                x = low_x[i]

                while i < len(low_x) and low_x[i] == x:
                    i += 1
                while j < len(high_x) and high_x[j] == x:
                    j += 1

                old_low = dp_low
                old_high = dp_high

                dp_low = max(old_low, old_high + 1 if old_high else 1)
                dp_high = max(old_high, old_low + 1 if old_low else 1)

        best = max(best, dp_low, dp_high)

    return best


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    out = []

    while pos < len(data):
        n = data[pos]
        pos += 1

        points = []
        for _ in range(n):
            x = data[pos]
            y = data[pos + 1]
            pos += 2
            points.append((x, y))

        out.append(str(solve_case(points)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()