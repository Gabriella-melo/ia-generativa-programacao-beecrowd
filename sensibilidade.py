"""Análise de sensibilidade citada na seção 4.6 do artigo.

Recalcula a aceitação na primeira tentativa sem as coletas em que a interface
acionou recursos por conta própria (registradas na coluna Observações da aba
Coleta de coleta_dados_experimento.xlsx):
  - ChatGPT, 1141, execução 1: busca na web ("Pesquisou 10 sites");
  - Claude, 2867, execução 1: execução de código ("Executou um comando") e raciocínio estendido;
  - Claude, 1032, 1033, 1243 e 1141, execução 1: raciocínio estendido ("Pensou por ...").

Requer: pandas, scipy, statsmodels. Uso: python sensibilidade.py
"""
import itertools
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint

T = ["chatgpt", "gemini", "claude"]
m = pd.read_csv("coletas_90.csv")

EXCLUIR = {
    (1141, "chatgpt", 1): "busca na web",
    (2867, "claude", 1): "execução de código e raciocínio estendido",
    (1032, "claude", 1): "raciocínio estendido",
    (1033, "claude", 1): "raciocínio estendido",
    (1243, "claude", 1): "raciocínio estendido",
    (1141, "claude", 1): "raciocínio estendido",
}
m["excluir"] = [(r.problema, r.ferramenta, r.execucao) in EXCLUIR for r in m.itertuples()]
s = m[~m.excluir]
print(f"Coletas excluídas: {int(m.excluir.sum())}")

# Aceitação na primeira tentativa, por ferramenta (com IC 95% de Wilson)
for t in T:
    d = s[s.ferramenta == t]
    k, n = int(d.aceito_1a.sum()), len(d)
    lo, hi = proportion_confint(k, n, method="wilson")
    print(f"{t}: {k}/{n} = {100 * k / n:.1f}% (IC 95%: {100 * lo:.1f}-{100 * hi:.1f})")

# Friedman com o problema como unidade: proporção de execuções aceitas entre as coletas restantes
a = s.groupby(["problema", "ferramenta"]).aceito_1a.mean().unstack()[T]
f = stats.friedmanchisquare(*[a[t] for t in T])
print(f"Friedman: chi2={f.statistic:.3f} p={f.pvalue:.4f} W={f.statistic / (len(a) * 2):.2f}")
print("Resumo por problema igual ao da análise principal:",
      a.equals(m.groupby(["problema", "ferramenta"]).aceito_1a.mean().unstack()[T]))

# McNemar exato por pares, sobre os pares (problema, execução) válidos para as duas ferramentas
w = s.pivot_table(index=["problema", "execucao"], columns="ferramenta", values="aceito_1a")
pares, ps = [], []
for x, y in itertools.combinations(T, 2):
    ww = w[[x, y]].dropna()
    tab = pd.crosstab(ww[x], ww[y]).reindex(index=[0, 1], columns=[0, 1], fill_value=0).values
    pares.append((x, y, len(ww)))
    ps.append(mcnemar(tab, exact=True).pvalue)
for (x, y, n), p, ph in zip(pares, ps, multipletests(ps, method="holm")[1]):
    print(f"McNemar {x} x {y} ({n} pares): p bruto={p:.4f}, Holm={ph:.3f}")
