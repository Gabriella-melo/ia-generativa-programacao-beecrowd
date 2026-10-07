import sys

dados = sys.stdin.buffer.read().split()
pos = 0
saida = []

while pos < len(dados):
    n = int(dados[pos])
    pos += 1

    melhor_d = 0
    melhor_t = 1

    for dia in range(1, n + 1):
        t = int(dados[pos])
        d = int(dados[pos + 1])
        pos += 2

        if dia == 1 or d * melhor_t > melhor_d * t:
            saida.append(str(dia))
            melhor_d = d
            melhor_t = t

sys.stdout.write("\n".join(saida))