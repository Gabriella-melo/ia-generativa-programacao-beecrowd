import sys

for line in sys.stdin:
    words = line.strip().split()
    total = 0
    count = 0

    for symbol in words:
        s = symbol[:-1] if symbol.endswith('.') else symbol

        if s and all(c.isalpha() and c.isascii() for c in s):
            total += len(s)
            count += 1

    average = total // count if count else 0

    if average <= 3:
        print(250)
    elif average <= 5:
        print(500)
    else:
        print(1000)
