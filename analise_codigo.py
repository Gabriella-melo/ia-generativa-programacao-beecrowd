#!/usr/bin/env python3
"""
Análise estática dos códigos gerados no experimento.

Uso:
    python analise_codigo.py <pasta_com_os_codigos>

Espera arquivos nomeados assim:  <id_problema>_<ferramenta>_<execucao>.py
Exemplos: 1050_chatgpt_1.py  ·  1050_gemini_1.py  ·  1050_claude_2.py
(o sufixo de execução é opcional; sem ele, a coluna Execução sai vazia)

Gera:  resultados_analise.csv  (na mesma pasta)
com as colunas na ordem da planilha de coleta:
    ID Problema · Ferramenta · Execução · Score Pylint · Complexidade ciclomática
    (total do arquivo) · Complexidade média das funções · Forma do código ·
    LOC · Densidade de comentários · Índice de manutenibilidade

A complexidade reportada é a TOTAL do arquivo (módulo + funções), única leitura
comparável entre ferramentas: não muda se o código é script linear ou está
encapsulado em funções.

Requer:  pip install pylint radon
"""

import csv
import io
import re
import sys
from pathlib import Path

try:
    from pylint.lint import Run
    from pylint.reporters.text import TextReporter
except ImportError:
    sys.exit("Pylint não encontrado. Rode: pip install pylint radon")

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    from radon.raw import analyze
    from radon.visitors import ComplexityVisitor
except ImportError:
    sys.exit("Radon não encontrado. Rode: pip install pylint radon")


def score_pylint(caminho):
    """Nota do Pylint de 0 a 10. Retorna None se não conseguir avaliar."""
    buffer = io.StringIO()
    try:
        resultado = Run(
            [
                str(caminho),
                "--disable=C0114,C0115,C0116",  # ignora falta de docstring
                # O nome do arquivo é convenção NOSSA (<id>_<ferramenta>_<execução>.py)
                # e começa por dígito, disparando C0103 (invalid-name) em todos os 90
                # arquivos. Como o escore do Pylint é normalizado pelo número de
                # instruções, essa penalidade constante pesa muito mais nos códigos
                # curtos do que nos longos: penalizaria as soluções concisas por causa
                # do nome que NÓS demos ao arquivo, não do código que a ferramenta
                # gerou. Medir isso seria medir o experimento, não o objeto.
                "--module-naming-style=any",
                # C0304 (missing-final-newline) mede o BOTÃO DE COPIAR da interface,
                # não o código que o modelo escreveu: nas 60 coletas conferidas, o
                # Gemini sempre entrega a quebra de linha final e o ChatGPT e o
                # Claude nunca entregam. A penalidade é constante por ferramenta
                # (-1,4 a -1,8 ponto em média para ChatGPT e Claude, zero para o
                # Gemini) e, como o escore é normalizado pelo número de instruções,
                # chega a -5,00 num arquivo de 2 instruções. Medir isso seria medir
                # o instrumento de coleta, não o objeto. Mesmo raciocínio do C0103.
                "--disable=C0304",
            ],
            reporter=TextReporter(buffer),
            exit=False,
        )
        nota = resultado.linter.stats.global_note
        return round(max(0.0, float(nota)), 2)
    except Exception as erro:  # noqa: BLE001
        print(f"  ! Pylint falhou em {caminho.name}: {erro}")
        return None


def metricas_radon(codigo):
    """Complexidade ciclomática média, LOC, densidade de comentários e MI."""
    resultado = {"cc_total": None, "cc_funcoes": None, "forma": None,
                 "loc": None, "comentarios": None, "mi": None}

    # A métrica principal é total_complexity: soma a complexidade do código de
    # nível de módulo com a das funções. É a ÚNICA leitura comparável entre
    # ferramentas, porque não muda conforme o código seja um script linear ou
    # esteja encapsulado em funções — dois códigos logicamente idênticos dão o
    # mesmo valor. cc_visit sozinho enxerga apenas funções e devolveria vazio
    # para os scripts lineares, que são a forma mais comum em juiz online.
    try:
        visitante = ComplexityVisitor.from_code(codigo)
        resultado["cc_total"] = visitante.total_complexity
        blocos = cc_visit(codigo)
        if blocos:
            resultado["cc_funcoes"] = round(
                sum(b.complexity for b in blocos) / len(blocos), 2)
            resultado["forma"] = "com funções"
        else:
            resultado["cc_funcoes"] = ""
            resultado["forma"] = "script linear"
    except Exception as erro:  # noqa: BLE001
        print(f"  ! Complexidade ciclomática falhou: {erro}")

    try:
        bruto = analyze(codigo)
        resultado["loc"] = bruto.sloc
        total = bruto.sloc + bruto.comments
        resultado["comentarios"] = round(bruto.comments / total, 4) if total else 0.0
    except Exception as erro:  # noqa: BLE001
        print(f"  ! Métricas brutas falharam: {erro}")

    try:
        resultado["mi"] = round(mi_visit(codigo, multi=True), 2)
    except Exception as erro:  # noqa: BLE001
        print(f"  ! Índice de manutenibilidade falhou: {erro}")

    return resultado


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    pasta = Path(sys.argv[1])
    if not pasta.is_dir():
        sys.exit(f"Pasta não encontrada: {pasta}")

    arquivos = sorted(pasta.glob("*.py"))
    if not arquivos:
        sys.exit(f"Nenhum arquivo .py em {pasta}")

    padrao = re.compile(r"^(?P<problema>[^_]+)_(?P<ferramenta>[^_]+)"
                        r"(?:_(?P<execucao>\d+))?$")
    linhas = []

    print(f"Analisando {len(arquivos)} arquivo(s)...\n")
    for arquivo in arquivos:
        print(f"→ {arquivo.name}")
        casado = padrao.match(arquivo.stem)
        if casado:
            problema = casado.group("problema")
            ferramenta = casado.group("ferramenta").replace("-", " ").title()
            execucao = casado.group("execucao") or ""
        else:
            problema, ferramenta, execucao = arquivo.stem, "?", ""
            print("  ! Nome fora do padrão <problema>_<ferramenta>_<execucao>.py")

        codigo = arquivo.read_text(encoding="utf-8", errors="replace")
        metricas = metricas_radon(codigo)
        nota = score_pylint(arquivo)

        linhas.append(
            {
                "ID Problema": problema,
                "Ferramenta": ferramenta,
                "Execucao": execucao,
                "Score Pylint": nota,
                "Complexidade ciclomatica": metricas["cc_total"],
                "Complexidade media das funcoes": metricas["cc_funcoes"],
                "Forma do codigo": metricas["forma"],
                "LOC": metricas["loc"],
                "Densidade de comentarios": metricas["comentarios"],
                "Indice de manutenibilidade": metricas["mi"],
                "Arquivo": arquivo.name,
            }
        )

    saida = pasta / "resultados_analise.csv"
    with saida.open("w", newline="", encoding="utf-8-sig") as destino:
        escritor = csv.DictWriter(destino, fieldnames=list(linhas[0].keys()))
        escritor.writeheader()
        escritor.writerows(linhas)

    print(f"\nPronto: {saida}")
    print("Abra no Excel e cole as colunas na aba Coleta da planilha.")
    print("Atenção: a densidade de comentários sai como fração (0,07 = 7%),")
    print("que é o formato que a planilha espera.")
    lineares = sum(1 for l in linhas if l["Forma do codigo"] == "script linear")
    print(f"\nScripts lineares (sem funções): {lineares} de {len(linhas)}.")
    print("Para esses, a complexidade reportada é a do módulo inteiro — cc_visit")
    print("sozinho devolveria vazio e a métrica se perderia.")


if __name__ == "__main__":
    main()
