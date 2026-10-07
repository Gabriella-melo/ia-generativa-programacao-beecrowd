import sys

def is_word(symbol):
    if not symbol:
        return False, 0
    if symbol.endswith('.'):
        letters = symbol[:-1]
    else:
        letters = symbol
    
    if len(letters) > 0 and letters.isalpha():
        return True, len(letters)
    return False, 0

def main():
    for line in sys.stdin:
        line = line.strip('\r\n')
        symbols = line.split()
        
        word_count = 0
        total_length = 0
        
        for symbol in symbols:
            valid, length = is_word(symbol)
            if valid:
                word_count += 1
                total_length += length
        
        if word_count == 0:
            avg_length = 0
        else:
            avg_length = total_length // word_count
        
        if avg_length <= 3:
            print(250)
        elif avg_length <= 5:
            print(500)
        else:
            print(1000)

if __name__ == '__main__':
    main()
