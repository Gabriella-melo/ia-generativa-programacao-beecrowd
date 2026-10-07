inter = gremio = empates = 0
grenais = 0

while True:
    inter_gols, gremio_gols = map(int, input().split())

    grenais += 1

    if inter_gols > gremio_gols:
        inter += 1
    elif gremio_gols > inter_gols:
        gremio += 1
    else:
        empates += 1

    print("Novo grenal (1-sim 2-nao)")
    resposta = int(input())

    if resposta == 2:
        break

print(f"{grenais} grenais")
print(f"Inter:{inter}")
print(f"Gremio:{gremio}")
print(f"Empates:{empates}")

if inter > gremio:
    print("Inter venceu mais")
elif gremio > inter:
    print("Gremio venceu mais")
else:
    print("Nao houve vencedor")