import sys

def main():
    input = sys.stdin.readline

    while True:
        line = input().split()
        if not line:
            break

        n, d = map(int, line)
        if n == 0 and d == 0:
            break

        s = input().strip()
        remove = d
        stack = []

        for ch in s:
            while remove > 0 and stack and stack[-1] < ch:
                stack.pop()
                remove -= 1
            stack.append(ch)

        if remove > 0:
            stack = stack[:-remove]

        print(''.join(stack))

if __name__ == "__main__":
    main()
