import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    ndata = len(data)
    out = []

    while idx < ndata:
        n = int(data[idx]); idx += 1
        pts = []
        for _ in range(n):
            x = int(data[idx]); y = int(data[idx+1]); idx += 2
            pts.append((x, y))

        if n == 0:
            out.append("0")
            continue

        pts.sort(key=lambda p: p[0])

        # group by x -> set of y values present at that x
        groups = []
        cur_x = pts[0][0]
        cur_set = set()
        for x, y in pts:
            if x != cur_x:
                groups.append(cur_set)
                cur_x = x
                cur_set = set()
            cur_set.add(y)
        groups.append(cur_set)

        distinct_ys = set(y for _, y in pts)

        best = 1  # a single point is always a valid wave

        for lo in distinct_ys:
            hi = lo + 2
            dpLo = 0
            dpHi = 0
            for g in groups:
                has_lo = lo in g
                has_hi = hi in g
                newDpLo = dpLo
                newDpHi = dpHi
                if has_lo:
                    cand = dpHi + 1
                    if cand > newDpLo:
                        newDpLo = cand
                if has_hi:
                    cand = dpLo + 1
                    if cand > newDpHi:
                        newDpHi = cand
                dpLo = newDpLo
                dpHi = newDpHi
            cur = dpLo if dpLo > dpHi else dpHi
            if cur > best:
                best = cur

        out.append(str(best))

    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))

if __name__ == "__main__":
    main()