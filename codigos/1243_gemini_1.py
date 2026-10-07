import sys

def solve():
    lines = sys.stdin.read().splitlines()
    for line in lines:
        symbols = line.split()
        word_count = 0
        total_length = 0

        for symbol in symbols:
            # Check if it ends with a single point
            has_dot = False
            if symbol.endswith('.'):
                has_dot = True
                symbol_letters = symbol[:-1]
            else:
                symbol_letters = symbol

            # Check if remaining characters are all letters (and non-empty)
            if len(symbol_letters) > 0 and symbol_letters.isalpha():
                word_count += 1
                total_length += len(symbol_letters)

        if word_count == 0:
            avg_length = 0
        else:
            avg_length = total_length // word_count

        if avg_length <= 3:
            print(250)
        elif avg_length in (4, 5):
            print(500)
        else:
            print(1000)

if __name__ == '__main__':
    solve()
