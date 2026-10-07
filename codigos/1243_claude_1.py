import sys
import re

def classify(line):
    words = line.split()
    total = 0
    count = 0
    for w in words:
        if re.fullmatch(r'[A-Za-z]+\.?', w):
            if w.endswith('.'):
                length = len(w) - 1
            else:
                length = len(w)
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