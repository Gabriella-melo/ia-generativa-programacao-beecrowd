import sys
import string

for line in sys.stdin:
    senha = line.rstrip('\n\r')

    valida = (
        6 <= len(senha) <= 32
        and any(c.isupper() for c in senha)
        and any(c.islower() for c in senha)
        and any(c.isdigit() for c in senha)
        and all(c in string.ascii_letters + string.digits for c in senha)
    )

    print("Senha valida." if valida else "Senha invalida.")
