# Dados e scripts do artigo "Ferramentas de IA generativa no apoio à programação"

Gabriella Bastos Melo e Isadora Vieira da Silva — Fatec Franca, 2026.

## O que há nesta pasta

| Arquivo | Conteúdo |
|---|---|
| `coletas_90.csv` | Uma linha por coleta (15 problemas × 3 ferramentas × 2 execuções): data, modelo exibido, vereditos das três tentativas, métricas de qualidade e tempo de execução. Inclui as variantes de sensibilidade do Pylint (sem C0303 e com verificação de docstring) e o índice de manutenibilidade sem o termo de comentários. |
| `tabela_por_problema.csv` | Tabela de resultados por problema e ferramenta (aceitações na 1ª tentativa e no final, de 0 a 2, e médias das métricas). |
| `mensagens_pylint.csv` | Todas as mensagens do Pylint por arquivo, com a categoria (convention, refactor, warning). |
| `metricas_codigo.py` | Recalcula Pylint e Radon sobre os 90 arquivos de `codigos/`. |
| `analise_revisada.py` | Reproduz todos os testes estatísticos do artigo a partir de `coletas_90.csv`. |

## O que incluir ao publicar (GitHub ou Zenodo)

Junte a esta pasta, a partir de `TCC-artigo/`:

- `coleta_dados_experimento.xlsx` (planilha original);
- `prompts/` (prompt padrão com cada enunciado e `prompt_correcao.txt`);
- `codigos/` (90 primeiras respostas e a subpasta `correcoes/`);
- `piloto_falhas_entrega.md`, `guia_coleta.md` e `problemas_selecionados.md` (protocolo).

## Configuração usada

- Python 3, Pylint 4.0.8 e Radon 6.0.1.
- Pylint: `--disable=C0114,C0115,C0116 --module-naming-style=any --disable=C0304`, com escores negativos tratados como zero.
- Radon: complexidade ciclomática total do arquivo; índice de manutenibilidade com `multi=True`.
- Unidade de análise: o problema (média ou soma das duas execuções); correção de Holm para as sete comparações principais.

Depois de publicar, substitua `[ENDEREÇO DO REPOSITÓRIO]` na seção 3.5 do artigo pelo link (ou DOI do Zenodo).
