import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        m = data[idx + 1]
        idx += 2

        coins = data[idx:idx + n]
        idx += n

        # Como 1 sempre existe, podemos usar programação dinâmica otimizada.
        # dp[x] = menor quantidade de blocos para formar x.
        # A quantidade de tipos é pequena (N <= 25) e ai <= 100.
        #
        # Em vez de testar todos os valores até M para cada moeda,
        # usamos a recorrência e percorremos apenas os tipos distintos.
        coins = sorted(set(coins), reverse=True)

        dp = [0] * (m + 1)
        INF = m + 1

        # Inicializa com a solução usando apenas blocos de tamanho 1.
        # Depois melhora com cada tipo de bloco.
        dp[:] = range(m + 1)

        for coin in coins:
            if coin == 1:
                continue

            # Processamento de moeda ilimitada.
            for x in range(coin, m + 1):
                candidate = dp[x - coin] + 1
                if candidate < dp[x]:
                    dp[x] = candidate

        ans.append(str(dp[m]))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()