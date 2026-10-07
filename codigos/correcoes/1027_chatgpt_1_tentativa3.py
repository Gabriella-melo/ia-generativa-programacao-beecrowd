import sys
from collections import defaultdict

def solve(points):
    if not points:
        return 0

    by_y = defaultdict(set)

    for x, y in points:
        by_y[y].add(x)

    ans = 0

    for y in by_y:
        upper = by_y.get(y + 2)
        if upper is None:
            continue

        lower = by_y[y]
        xs = sorted(lower | upper)

        low = 0
        high = 0

        for x in xs:
            old_low = low
            old_high = high

            if x in lower:
                low = max(old_low, old_high + 1)

            if x in upper:
                high = max(old_high, old_low + 1)

        ans = max(ans, low, high)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    idx = 0
    results = []

    while idx < len(data):
        n = data[idx]
        idx += 1

        points = []
        for _ in range(n):
            x = data[idx]
            y = data[idx + 1]
            idx += 2
            points.append((x, y))

        results.append(str(solve(points)))

    sys.stdout.write("\n".join(results) + ("\n" if results else ""))


if __name__ == "__main__":
    main()