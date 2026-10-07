import sys

def main():
    data = sys.stdin.read().split('\n')
    idx = 0
    n = int(data[idx].strip()); idx += 1
    results = []
    for _ in range(n):
        s = data[idx].strip(); idx += 1
        k = int(data[idx].strip()); idx += 1
        decoded = []
        for ch in s:
            new_ord = (ord(ch) - ord('A') - k) % 26
            decoded.append(chr(new_ord + ord('A')))
        results.append(''.join(decoded))
    print('\n'.join(results))

if __name__ == '__main__':
    main()