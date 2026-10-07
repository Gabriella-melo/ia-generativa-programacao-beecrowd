import sys

def main():
    for line in sys.stdin:
        s = line.rstrip('\r\n')
        
        if not (6 <= len(s) <= 32):
            print("Senha invalida.")
            continue
            
        has_upper = False
        has_lower = False
        has_digit = False
        is_valid_chars = True
        
        for char in s:
            if 'a' <= char <= 'z':
                has_lower = True
            elif 'A' <= char <= 'Z':
                has_upper = True
            elif '0' <= char <= '9':
                has_digit = True
            else:
                is_valid_chars = False
                break
                
        if is_valid_chars and has_upper and has_lower and has_digit:
            print("Senha valida.")
        else:
            print("Senha invalida.")

if __name__ == '__main__':
    main()
