import sys

def solve():
    data = sys.stdin.buffer.read().split()
    i = 0
    output = []

    while i < len(data):
        n = int(data[i])
        d = int(data[i + 1])
        i += 2

        if n == 0 and d == 0:
            break

        number = data[i].decode()
        i += 1

        remove = d
        stack = []

        for digit in number:
            while stack and remove > 0 and stack[-1] < digit:
                stack.pop()
                remove -= 1
            stack.append(digit)

        if remove > 0:
            stack = stack[:-remove]

        output.append(''.join(stack))

    sys.stdout.write('\n'.join(output))

if __name__ == "__main__":
    solve()