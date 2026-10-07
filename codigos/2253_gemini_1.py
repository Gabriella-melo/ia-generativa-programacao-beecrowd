import sys

def solve():
    for line in sys.stdin:
        s = line.rstrip('\r\n')
        
        # Check length requirement: 6 to 32 characters
        if not (6 <= len(s) <= 32):
            print("Senha invalida.")
            continue
        
        has_upper = False
        has_lower = False
        has_digit = False
        is_valid = True
        
        for ch in s:
            if ch.isupper():
                has_upper = True
            elif ch.islower():
                has_lower = True
            elif ch.isdigit():
                has_digit = True
            else:
                # Any character that is not uppercase, lowercase, or a digit is invalid
                is_valid = False
                break
                
        if is_valid and has_upper and has_lower and has_digit:
            print("Senha valida.")
        else:
            print("Senha invalida.")

if __name__ == '__main__':
    solve()
