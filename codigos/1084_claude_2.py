import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    out = []
    while True:
        n = int(input_data[idx]); d = int(input_data[idx+1]); idx += 2
        if n == 0 and d == 0:
            break
        s = input_data[idx]; idx += 1
        keep = n - d
        stack = []
        to_remove = d
        for ch in s:
            while stack and to_remove > 0 and stack[-1] < ch:
                stack.pop()
                to_remove -= 1
            stack.append(ch)
        result = stack[:keep]
        out.append(''.join(result))
    print('\n'.join(out))

solve()