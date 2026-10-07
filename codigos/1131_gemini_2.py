import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    total_grenais = 0
    inter_wins = 0
    gremio_wins = 0
    draws = 0

    while idx < len(input_data):
        inter_goals = int(input_data[idx])
        gremio_goals = int(input_data[idx + 1])
        idx += 2

        total_grenais += 1
        if inter_goals > gremio_goals:
            inter_wins += 1
        elif gremio_goals > inter_goals:
            gremio_wins += 1
        else:
            draws += 1

        print("Novo grenal (1-sim 2-nao)")

        if idx < len(input_data):
            op = int(input_data[idx])
            idx += 1
            if op == 2:
                break

    print(f"{total_grenais} grenais")
    print(f"Inter:{inter_wins}")
    print(f"Gremio:{gremio_wins}")
    print(f"Empates:{draws}")

    if inter_wins > gremio_wins:
        print("Inter venceu mais")
    elif gremio_wins > inter_wins:
        print("Gremio venceu mais")
    else:
        print("Não houve vencedor")

if __name__ == '__main__':
    main()
