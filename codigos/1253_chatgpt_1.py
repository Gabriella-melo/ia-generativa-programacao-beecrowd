n = int(input())

for _ in range(n):
    text = input().strip()
    shift = int(input())
    
    decoded = ''.join(
        chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        for c in text
    )
    
    print(decoded)