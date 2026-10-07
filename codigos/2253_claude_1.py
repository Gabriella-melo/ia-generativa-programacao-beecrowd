import sys
import re

def valid(s):
    if len(s) < 6 or len(s) > 32:
        return False
    if not re.match(r'^[A-Za-z0-9]+$', s):
        return False
    if not re.search(r'[A-Z]', s):
        return False
    if not re.search(r'[a-z]', s):
        return False
    if not re.search(r'[0-9]', s):
        return False
    return True

def main():
    out = []
    for line in sys.stdin:
        s = line.rstrip('\n')
        if s == '' and line == '':
            continue
        if valid(s):
            out.append("Senha valida.")
        else:
            out.append("Senha invalida.")
    print('\n'.join(out))

if __name__ == '__main__':
    main()