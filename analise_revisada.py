"""Reproduz as análises do artigo a partir de coletas_90.csv.
Requer: pandas, scipy, statsmodels.  Uso: python analise_revisada.py"""
import itertools, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.contingency_tables import mcnemar, cochrans_q
warnings.filterwarnings("ignore")
T = ["chatgpt", "gemini", "claude"]
m = pd.read_csv("coletas_90.csv")
m["tempo_s"] = pd.to_numeric(m.tempo_s, errors="coerce")
m["coment"] = m.densidade_comentarios * 100
def W(chi, n, k=3): return chi / (n * (k - 1))
def rrb(x, y):  # correlação bisserial de postos pareada
    d = np.asarray(x) - np.asarray(y); d = d[d != 0]
    r = stats.rankdata(np.abs(d)); return (r[d > 0].sum() - r[d < 0].sum()) / r.sum()
def bloco(col):  # média por problema (unidade de análise)
    return m.groupby(["problema", "ferramenta"])[col].mean().unstack()[T]
omni = {}
# QP1 aceitação: soma 0-2 por problema
a = m.groupby(["problema", "ferramenta"]).aceito_1a.sum().unstack()[T]
f = stats.friedmanchisquare(*[a[t] for t in T]); omni["aceitacao"] = f.pvalue
print(f"Aceitação 1a: Friedman chi2={f.statistic:.3f} p={f.pvalue:.4f} W={W(f.statistic,15):.2f}")
for e in (1, 2):
    w = m[m.execucao == e].pivot_table(index="problema", columns="ferramenta", values="aceito_1a")[T]
    q = cochrans_q(w.values); print(f"  execução {e}: Q={q.statistic:.3f} p={q.pvalue:.4f}")
w = m.pivot_table(index=["problema", "execucao"], columns="ferramenta", values="aceito_1a")[T]
ps = []
for x, y in itertools.combinations(T, 2):
    tab = pd.crosstab(w[x], w[y]).reindex(index=[0, 1], columns=[0, 1], fill_value=0).values
    ps.append(mcnemar(tab, exact=True).pvalue)
print("  McNemar exato (Holm):", dict(zip(map(str, itertools.combinations(T, 2)), np.round(multipletests(ps, method='holm')[1], 3))))
# QP3 métricas
for col in ["pylint", "cc_total", "mi", "loc", "coment"]:
    b = bloco(col); f = stats.friedmanchisquare(*[b[t] for t in T]); omni[col] = f.pvalue
    pp = [stats.wilcoxon(b[x], b[y]).pvalue for x, y in itertools.combinations(T, 2)]
    print(f"{col}: chi2={f.statistic:.3f} p={f.pvalue:.4f} W={W(f.statistic,15):.2f} | pares Holm {np.round(multipletests(pp,method='holm')[1],4)} r={[round(rrb(b[x],b[y]),2) for x,y in itertools.combinations(T,2)]}")
for col in ["pylint_sem_C0303", "pylint_com_docstring", "mi_sem_comentarios"]:
    b = bloco(col); f = stats.friedmanchisquare(*[b[t] for t in T])
    print(f"  sensibilidade {col}: médias {m.groupby('ferramenta')[col].mean()[T].round(2).tolist()} p={f.pvalue:.4f}")
# tempo: soluções aceitas no final, blocos completos, média por problema
s = m[m.resultado_final == "Accepted"].pivot_table(index=["problema", "execucao"], columns="ferramenta", values="tempo_s")[T].dropna()
tp = s.groupby(level=0).mean(); f = stats.friedmanchisquare(*[tp[t] for t in T]); omni["tempo"] = f.pvalue
print(f"Tempo: {len(s)} blocos, {len(tp)} problemas, chi2={f.statistic:.3f} p={f.pvalue:.4f} W={W(f.statistic,len(tp)):.2f}")
print("Holm (7 comparações):", dict(zip(omni, np.round(multipletests(list(omni.values()), method='holm')[1], 4))))
# qualidade x corretude por coleta (GEE, problema como agrupamento)
for col in ["pylint", "mi"]:
    m["z"] = (m[col] - m[col].mean()) / m[col].std()
    g = smf.gee("aceito_1a ~ z + C(ferramenta)", groups="problema", data=m, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
    g2 = smf.gee("aceito_1a ~ z + C(ferramenta) + C(faixa)", groups="problema", data=m, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
    print(f"GEE {col}: OR={np.exp(g.params['z']):.2f} p={g.pvalues['z']:.3f} | ajustado pela faixa p={g2.pvalues['z']:.3f}")
print("Consistência 12/15 vs 15/15, Fisher p =", round(stats.fisher_exact([[12, 3], [15, 0]])[1], 3))
