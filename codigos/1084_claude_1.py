import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    out = []
    while idx < len(data):
        n = int(data[idx]); d = int(data[idx+1]); idx += 2
        if n == 0 and d == 0:
            break
        num = data[idx]; idx += 1
        keep = n - d
        stack = []
        to_remove = d
        for c in num:
            while stack and to_remove > 0 and stack[-1] < c:
                stack.pop()
                to_remove -= 1
            stack.append(c)
        result = stack[:keep]
        out.append(''.join(result))
    print('\n'.join(out))

solve()