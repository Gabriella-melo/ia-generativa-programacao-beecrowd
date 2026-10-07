import sys
import re

pattern = re.compile(r'^[A-Za-z]+\.?$')

def classify(line):
    tokens = line.split()
    total = 0
    count = 0
    for tok in tokens:
        if pattern.match(tok):
            length = len(tok) - (1 if tok.endswith('.') else 0)
            total += length
            count += 1
    avg = total // count if count > 0 else 0
    if avg <= 3:
        return 250
    elif avg <= 5:
        return 500
    else:
        return 1000

def main():
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line == '' and False:
            continue
        print(classify(line))

if __name__ == '__main__':
    main()