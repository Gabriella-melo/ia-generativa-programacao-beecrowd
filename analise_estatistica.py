#!/usr/bin/env python3
"""
Análise estatística dos resultados do experimento.

Uso:
    python analise_estatistica.py coleta_dados_experimento.xlsx

Lê a aba "Coleta" e produz:
  · estatística descritiva por ferramenta (n, média, mediana, desvio-padrão)
  · teste de normalidade (Shapiro-Wilk)
  · teste omnibus para medidas repetidas (Friedman para métricas contínuas,
    Q de Cochran para a métrica binária "Aceito na 1ª tentativa")
  · taxa de autocorreção e tipologia dos vereditos por ferramenta
  · comparações par a par (Wilcoxon pareado, com correção de Bonferroni)
  · tamanho de efeito (delta de Cliff)
  · um bloco de texto pronto para colar na seção de resultados

Por que estes testes: o desenho é de MEDIDAS REPETIDAS — os mesmos 15 problemas
são submetidos às três ferramentas, em duas execuções. Cada par
(problema, execução) é um bloco. Testes para amostras independentes, como o
Mann-Whitney, seriam inadequados aqui porque ignorariam esse pareamento.

Requer:  pip install pandas scipy openpyxl
"""

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ALFA = 0.05

METRICAS = [
    ("Rodadas até Accepted (1-3)", "menor é melhor"),
    ("Score Pylint (0-10)", "maior é melhor"),
    ("Complexidade ciclomática (total)", "menor é melhor"),
    ("Índice de manutenibilidade", "maior é melhor"),
    ("LOC", "menor é melhor"),
    ("Densidade de comentários (%)", "—"),
    ("Tempo de execução (s)", "menor é melhor"),
]

# Não há métrica de tempo de interação: o estudo mede apenas o que é registrado
# automaticamente por sistema — veredito do juiz, análise estática e tempo de
# execução do programa. Nenhum dado depende de cronometragem humana.


def cliffs_delta(a, b):
    """Delta de Cliff e sua interpretação (Romano et al., 2006)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    maior = sum((x > y) for x in a for y in b)
    menor = sum((x < y) for x in a for y in b)
    delta = (maior - menor) / (len(a) * len(b))
    d = abs(delta)
    if d < 0.147:
        rotulo = "desprezível"
    elif d < 0.33:
        rotulo = "pequeno"
    elif d < 0.474:
        rotulo = "médio"
    else:
        rotulo = "grande"
    return delta, rotulo


def cochran_q(matriz):
    """Q de Cochran para k tratamentos pareados com desfecho binário."""
    m = np.asarray(matriz, float)
    n, k = m.shape
    col = m.sum(axis=0)
    lin = m.sum(axis=1)
    total = m.sum()
    denom = k * total - np.sum(lin ** 2)
    if denom == 0:
        return float("nan"), float("nan")
    q = (k - 1) * (k * np.sum(col ** 2) - total ** 2) / denom
    p = stats.chi2.sf(q, k - 1)
    return q, p


def blocos(df, coluna, ferramentas):
    """Matriz (blocos × ferramentas) com apenas os blocos completos."""
    pivo = df.pivot_table(index=["ID Problema", "Execução"],
                          columns="Ferramenta", values=coluna, aggfunc="first")
    faltando = [f for f in ferramentas if f not in pivo.columns]
    if faltando:
        return None
    pivo = pivo[ferramentas].dropna()
    return pivo


def formatar_p(p):
    if np.isnan(p):
        return "n/d"
    return "< 0,001" if p < 0.001 else f"= {p:.3f}".replace(".", ",")


def analisar(caminho):
    df = pd.read_excel(caminho, sheet_name="Coleta")
    if "Observações" in df.columns:  # descarta a linha de exemplo da planilha
        df = df[~df["Observações"].astype(str).str.contains("EXEMPLO", na=False)]
    df = df[df["Resultado final"].notna()]
    if df.empty:
        sys.exit("Nenhuma linha preenchida na aba Coleta ainda.")

    ferramentas = [f for f in df["Ferramenta"].dropna().unique()]
    print("=" * 74)
    print("ANÁLISE ESTATÍSTICA — experimento de IA generativa na programação")
    print("=" * 74)
    print(f"\nFerramentas: {', '.join(ferramentas)}")
    print(f"Coletas preenchidas: {len(df)} de 90")
    for f in ferramentas:
        sub = df[df["Ferramenta"] == f]
        print(f"  · {f}: {len(sub)} coletas")

    # ---------- corretude ----------
    print("\n" + "-" * 74)
    print("1. CORRETUDE")
    print("-" * 74)
    if "Aceito na 1ª tentativa" in df.columns:
        df["_aceito"] = (df["Aceito na 1ª tentativa"].astype(str).str.strip()
                         .str.lower().map({"sim": 1, "não": 0, "nao": 0}))
        for f in ferramentas:
            sub = df[(df["Ferramenta"] == f) & df["_aceito"].notna()]
            if len(sub):
                print(f"  {f:12s} aceito na 1ª tentativa: "
                      f"{sub['_aceito'].mean():.1%} ({int(sub['_aceito'].sum())}/{len(sub)})")
        m = blocos(df, "_aceito", ferramentas)
        if m is not None and len(m) >= 3:
            q, p = cochran_q(m.values)
            print(f"\n  Q de Cochran (k={len(ferramentas)}, blocos={len(m)}): "
                  f"Q = {q:.3f}, p {formatar_p(p)}")
            print("  → " + ("há diferença significativa entre as ferramentas"
                            if p < ALFA else
                            "não há diferença estatisticamente significativa"))
        else:
            print("\n  (blocos completos insuficientes para o Q de Cochran)")

    # ---------- autocorreção ----------
    print("\n" + "-" * 74)
    print("2. AUTOCORREÇÃO (o que acontece após o veredito de erro voltar)")
    print("-" * 74)
    col_v = "Veredito 1ª tentativa"
    # A autocorreção só existe onde houve veredito de erro do juiz para realimentar.
    # Coletas marcadas como "Não extraível" — a ferramenta não entregou código
    # utilizável — nunca chegaram ao juiz, e por isso ficam fora do denominador:
    # contá-las aqui atribuiria à ferramenta uma falha de autocorreção que ela nunca
    # teve a chance de cometer. Elas continuam contando na corretude (Resultado
    # final = Falha) e são reportadas em bloco próprio, logo abaixo.
    if col_v in df.columns:
        nao_extraivel = df[col_v].astype(str).str.strip() == "Não extraível"
    else:
        nao_extraivel = pd.Series(False, index=df.index)

    if "_aceito" in df.columns:
        for f in ferramentas:
            falhou = df[(df["Ferramenta"] == f) & (df["_aceito"] == 0) & ~nao_extraivel]
            if len(falhou):
                recuperou = (falhou["Resultado final"] == "Accepted").sum()
                print(f"  {f:12s} falhou de primeira em {len(falhou):2d} casos, "
                      f"recuperou {recuperou:2d} → {recuperou/len(falhou):.1%}")
            else:
                print(f"  {f:12s} nenhuma falha de primeira tentativa com veredito do juiz")

    # ---------- falhas de entrega ----------
    if nao_extraivel.any():
        print("\n" + "-" * 74)
        print("2b. FALHAS DE ENTREGA (código não extraível da resposta)")
        print("-" * 74)
        for f in ferramentas:
            n = int((nao_extraivel & (df["Ferramenta"] == f)).sum())
            total = int((df["Ferramenta"] == f).sum())
            print(f"  {f:12s} {n} de {total} coletas")
        print("\n  A ferramenta devolveu a solução parcialmente fora do bloco de código,")
        print("  com a indentação colapsada pela renderização e irrecuperável na cópia.")
        print("  Contam como Falha na corretude e ficam fora do cálculo de autocorreção,")
        print("  porque nunca houve veredito do juiz para realimentar.")

    # ---------- tipologia dos vereditos ----------
    if col_v in df.columns and df[col_v].notna().any():
        print("\n" + "-" * 74)
        print("3. TIPOLOGIA DOS VEREDITOS NA 1ª TENTATIVA")
        print("-" * 74)
        tabela = pd.crosstab(df[col_v], df["Ferramenta"])
        for f in ferramentas:
            if f not in tabela.columns:
                tabela[f] = 0
        print(tabela[ferramentas].to_string())
        print("\n  Como cada ferramenta falha é achado qualitativo — Billah et al. (2024)")
        print("  relataram que Gemini e Meta AI falhavam em gerar código compilável,")
        print("  enquanto o ChatGPT estourava o limite de tempo.")

    # ---------- métricas contínuas ----------
    print("\n" + "-" * 74)
    print("4. MÉTRICAS CONTÍNUAS")
    print("-" * 74)

    linhas_artigo = []
    for coluna, sentido in METRICAS:
        if coluna not in df.columns or df[coluna].notna().sum() == 0:
            continue
        print(f"\n### {coluna}  ({sentido})")

        for f in ferramentas:
            v = pd.to_numeric(df[df["Ferramenta"] == f][coluna],
                              errors="coerce").dropna()
            if len(v) == 0:
                continue
            sw = ("n/d" if len(v) < 3
                  else formatar_p(stats.shapiro(v).pvalue))
            print(f"  {f:12s} n={len(v):3d}  média={v.mean():8.2f}  "
                  f"mediana={v.median():8.2f}  dp={v.std(ddof=1):7.2f}  "
                  f"Shapiro-Wilk p {sw}")

        m = blocos(df, coluna, ferramentas)
        if m is None or len(m) < 3:
            print("  (blocos completos insuficientes para o teste omnibus)")
            continue

        fr = stats.friedmanchisquare(*[m[f].values for f in ferramentas])
        print(f"\n  Friedman (blocos={len(m)}): χ² = {fr.statistic:.3f}, "
              f"p {formatar_p(fr.pvalue)}")

        if fr.pvalue < ALFA:
            print("  → diferença significativa; comparações par a par:")
            pares = list(combinations(ferramentas, 2))
            bonf = ALFA / len(pares)
            for a, b in pares:
                try:
                    w = stats.wilcoxon(m[a].values, m[b].values)
                    pw = w.pvalue
                except ValueError:
                    pw = float("nan")
                delta, rotulo = cliffs_delta(m[a].values, m[b].values)
                marca = "*" if (not np.isnan(pw) and pw < bonf) else " "
                print(f"    {marca} {a} x {b}: Wilcoxon p {formatar_p(pw)}  |  "
                      f"delta de Cliff = {delta:+.3f} ({rotulo})")
            print(f"    (* significativo com Bonferroni: α = {bonf:.4f})")
            linhas_artigo.append(
                f"{coluna}: diferença significativa entre as ferramentas "
                f"(Friedman, χ² = {fr.statistic:.2f}, p {formatar_p(fr.pvalue)}).")
        else:
            print("  → não há diferença estatisticamente significativa")
            linhas_artigo.append(
                f"{coluna}: sem diferença estatisticamente significativa "
                f"(Friedman, χ² = {fr.statistic:.2f}, p {formatar_p(fr.pvalue)}).")

    # ---------- forma do código ----------
    if "Forma do código" in df.columns and df["Forma do código"].notna().any():
        print("\n" + "-" * 74)
        print("5. FORMA DO CÓDIGO GERADO")
        print("-" * 74)
        for f in ferramentas:
            sub = df[(df["Ferramenta"] == f) & df["Forma do código"].notna()]
            if len(sub):
                cont = sub["Forma do código"].value_counts()
                partes = ", ".join(f"{k}: {v}" for k, v in cont.items())
                print(f"  {f:12s} {partes}")
        print("  (diferença de estilo entre ferramentas — material para a discussão)")

    # ---------- consistência ----------
    print("\n" + "-" * 74)
    print("6. CONSISTÊNCIA ENTRE AS DUAS EXECUÇÕES")
    print("-" * 74)
    if "_aceito" in df.columns and df["Execução"].nunique() == 2:
        for f in ferramentas:
            sub = df[df["Ferramenta"] == f]
            p1 = sub[sub["Execução"] == 1].set_index("ID Problema")["_aceito"]
            p2 = sub[sub["Execução"] == 2].set_index("ID Problema")["_aceito"]
            comuns = p1.index.intersection(p2.index)
            if len(comuns):
                igual = (p1[comuns] == p2[comuns]).mean()
                print(f"  {f:12s} desfecho idêntico nas duas execuções: "
                      f"{igual:.1%} ({int((p1[comuns] == p2[comuns]).sum())}/{len(comuns)})")
    else:
        print("  (é preciso ter as duas execuções preenchidas)")

    if linhas_artigo:
        print("\n" + "=" * 74)
        print("RESUMO PARA A SEÇÃO DE RESULTADOS")
        print("=" * 74)
        for linha in linhas_artigo:
            print(f"  · {linha}")

    print("\nLembre-se: 'sem diferença significativa' é um resultado legítimo "
          "e deve ser\nreportado como tal — Licorish et al. (2025) encontraram "
          "exatamente isso no Pylint\n(p = 0,64).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    arquivo = Path(sys.argv[1])
    if not arquivo.exists():
        sys.exit(f"Arquivo não encontrado: {arquivo}")
    analisar(arquivo)
