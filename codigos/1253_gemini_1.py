import sys

def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    n = int(input_data[0])
    idx = 1
    
    for _ in range(n):
        if idx >= len(input_data):
            break
        text = input_data[idx]
        shift = int(input_data[idx + 1])
        idx += 2
        
        decoded = []
        for char in text:
            if 'A' <= char <= 'Z':
                # Shift backwards by 'shift' places to decode
                decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                decoded.append(decoded_char)
            else:
                decoded.append(char)
                
        print("".join(decoded))

if __name__ == "__main__":
    main()
