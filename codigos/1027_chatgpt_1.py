import sys
from collections import defaultdict

def solve(points):
    by_y = defaultdict(dict)

    for x, y in points:
        by_y[y][x] = True

    best = 0

    for y in by_y:
        if y + 2 not in by_y:
            continue

        lower = by_y[y]
        upper = by_y[y + 2]

        xs = sorted(set(lower) | set(upper))

        dp_low = 0
        dp_high = 0

        for x in xs:
            old_low = dp_low
            old_high = dp_high

            if x in lower:
                dp_low = max(old_low, old_high + 1)

            if x in upper:
                dp_high = max(old_high, old_low + 1)

        best = max(best, dp_low, dp_high)

    return best


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    output = []

    while pos < len(data):
        n = data[pos]
        pos += 1

        points = []
        for _ in range(n):
            x = data[pos]
            y = data[pos + 1]
            pos += 2
            points.append((x, y))

        output.append(str(solve(points)))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
