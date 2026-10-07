import sys

def main():
    input = sys.stdin.readline

    while True:
        n, d = map(int, input().split())

        if n == 0 and d == 0:
            break

        number = input().strip()

        stack = []
        removed = 0

        for digit in number:
            while stack and removed < d and stack[-1] < digit:
                stack.pop()
                removed += 1
            stack.append(digit)

        if removed < d:
            stack = stack[:-(d - removed)]

        print(''.join(stack))


if __name__ == "__main__":
    main()