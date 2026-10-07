import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    length = len(data)
    results = []
    while idx < length:
        n = int(data[idx]); idx += 1
        points = []
        for _ in range(n):
            x = int(data[idx]); y = int(data[idx + 1])
            idx += 2
            points.append((x, y))

        points_by_y = {}
        for x, y in points:
            if y in points_by_y:
                points_by_y[y].append(x)
            else:
                points_by_y[y] = [x]

        candidates = set()
        for y in points_by_y:
            candidates.add(y - 1)
            candidates.add(y + 1)

        best = 0
        for a in candidates:
            low_y = a - 1
            high_y = a + 1
            xs = {}

            low_list = points_by_y.get(low_y)
            if low_list:
                for x in low_list:
                    if x in xs:
                        xs[x] |= 1
                    else:
                        xs[x] = 1

            high_list = points_by_y.get(high_y)
            if high_list:
                for x in high_list:
                    if x in xs:
                        xs[x] |= 2
                    else:
                        xs[x] = 2

            if not xs:
                continue

            sorted_x = sorted(xs.keys())
            dp_low = 0
            dp_high = 0
            for x in sorted_x:
                t = xs[x]
                old_low = dp_low
                old_high = dp_high
                if t & 1:
                    nl = old_high + 1
                    if nl > dp_low:
                        dp_low = nl
                if t & 2:
                    nh = old_low + 1
                    if nh > dp_high:
                        dp_high = nh

            cur = dp_low if dp_low > dp_high else dp_high
            if cur > best:
                best = cur

        results.append(str(best))

    sys.stdout.write('\n'.join(results) + ('\n' if results else ''))

if __name__ == "__main__":
    main()