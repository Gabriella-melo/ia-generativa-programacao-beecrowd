import sys

for line in sys.stdin:
    senha = line.rstrip('\n\r')
    
    valida = (
        6 <= len(senha) <= 32
        and any(c.isupper() for c in senha)
        and any(c.islower() for c in senha)
        and any(c.isdigit() for c in senha)
        and all(('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9') for c in senha)
    )
    
    print("Senha valida." if valida else "Senha invalida.")