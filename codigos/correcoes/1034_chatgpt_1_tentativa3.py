import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    results = []

    for _ in range(t):
        n = data[pos]
        m = data[pos + 1]
        pos += 2

        coins = list(set(data[pos:pos + n]))
        pos += n

        if m == 0:
            results.append("0")
            continue

        max_coin = max(coins)

        # Para valores suficientemente grandes, uma solução ótima
        # sempre pode ser obtida acrescentando um bloco de tamanho max_coin.
        # Como max_coin <= 100, basta calcular até um limite pequeno.
        limit = min(m, 2 * max_coin * max_coin + max_coin)

        INF = limit + 1
        dp = [INF] * (limit + 1)
        dp[0] = 0

        # Processa cada valor apenas uma vez. Como 1 está presente,
        # todos os valores são alcançáveis.
        for x in range(1, limit + 1):
            best = INF
            for c in coins:
                if c > x:
                    continue
                v = dp[x - c] + 1
                if v < best:
                    best = v
            dp[x] = best

        if m <= limit:
            results.append(str(dp[m]))
        else:
            # Após o limite, dp[x + max_coin] = dp[x] + 1.
            q, r = divmod(m - limit, max_coin)
            target = limit + r

            # target pode ultrapassar limit em até max_coin-1.
            # Calculamos essa pequena faixa diretamente.
            extra_dp = dp[:]
            end = limit + max_coin - 1

            if len(extra_dp) <= end:
                extra_dp.extend([INF] * (end + 1 - len(extra_dp)))

            for x in range(limit + 1, end + 1):
                best = INF
                for c in coins:
                    if c <= x:
                        v = extra_dp[x - c] + 1
                        if v < best:
                            best = v
                extra_dp[x] = best

            results.append(str(extra_dp[target] + q))

    sys.stdout.write("\n".join(results))

if __name__ == "__main__":
    main()