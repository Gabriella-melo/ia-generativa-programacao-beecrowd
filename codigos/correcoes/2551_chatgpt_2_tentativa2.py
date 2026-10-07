import sys

entrada = sys.stdin.buffer.read().split()
i = 0
saida = []

while i < len(entrada):
    n = int(entrada[i])
    i += 1

    record_speed = 0.0

    for dia in range(1, n + 1):
        t = int(entrada[i])
        d = int(entrada[i + 1])
        i += 2

        velocidade = d / t

        if dia == 1 or velocidade > record_speed:
            saida.append(str(dia))
            record_speed = velocidade

sys.stdout.write("\n".join(saida))