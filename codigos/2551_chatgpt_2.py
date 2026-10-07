import sys

data = list(map(int, sys.stdin.buffer.read().split()))
pos = 0
out = []

while pos < len(data):
    n = data[pos]
    pos += 1

    best_num = None
    best_den = None

    for day in range(1, n + 1):
        t = data[pos]
        d = data[pos + 1]
        pos += 2

        if day == 1:
            out.append("1")
            best_num = d
            best_den = t
        elif d * best_den > best_num * t:
            out.append(str(day))
            best_num = d
            best_den = t

sys.stdout.write("\n".join(out))