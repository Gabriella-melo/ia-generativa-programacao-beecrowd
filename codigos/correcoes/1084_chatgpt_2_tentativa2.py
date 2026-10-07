import sys

def main():
    lines = sys.stdin.buffer.read().split()
    pos = 0
    out = []

    while pos < len(lines):
        n = int(lines[pos])
        d = int(lines[pos + 1])
        pos += 2

        if n == 0 and d == 0:
            break

        number = lines[pos].decode()
        pos += 1

        stack = []
        to_remove = d

        for digit in number:
            while stack and to_remove > 0 and stack[-1] < digit:
                stack.pop()
                to_remove -= 1
            stack.append(digit)

        if to_remove > 0:
            stack = stack[:-to_remove]

        out.append(''.join(stack))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()