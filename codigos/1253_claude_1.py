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
            new_ch = chr((ord(ch) - ord('A') - k) % 26 + ord('A'))
            decoded.append(new_ch)
        results.append(''.join(decoded))
    print('\n'.join(results))

if __name__ == '__main__':
    main()