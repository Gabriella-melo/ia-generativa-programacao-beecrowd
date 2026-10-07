import sys
import re

def valida(s):
    if not (6 <= len(s) <= 32):
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

for line in sys.stdin:
    s = line.rstrip('\n').rstrip('\r')
    if s == '' and line == '':
        continue
    if valida(s):
        print("Senha valida.")
    else:
        print("Senha invalida.")