import sys

for line in sys.stdin:
    symbols = line.strip().split()
    lengths = []

    for symbol in symbols:
        word = symbol
        if word.endswith('.'):
            word = word[:-1]

        if word and all(c.isalpha() for c in word):
            lengths.append(len(word))

    if lengths:
        avg = sum(lengths) // len(lengths)
    else:
        avg = 0

    if avg <= 3:
        print(250)
    elif avg <= 5:
        print(500)
    else:
        print(1000)