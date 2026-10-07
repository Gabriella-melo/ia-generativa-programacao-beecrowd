n = int(input())

for _ in range(n):
    texto = input().strip()
    deslocamento = int(input())

    resultado = ''.join(
        chr((ord(c) - ord('A') - deslocamento) % 26 + ord('A'))
        for c in texto
    )

    print(resultado)