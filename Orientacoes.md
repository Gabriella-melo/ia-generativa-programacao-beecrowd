# Ferramentas de IA generativa no apoio à programação

Dados, prompts, códigos e scripts do artigo *Ferramentas de IA generativa no apoio à programação: uma análise comparativa da corretude, da autocorreção, da qualidade e da consistência do código gerado* (Gabriella Bastos Melo e Isadora Vieira da Silva, Fatec Franca, 2026).

O experimento submeteu 15 problemas do juiz online Beecrowd ao ChatGPT (GPT-5.6 Luna), ao Gemini (Gemini 3.6 Flash) e ao Claude (Claude Sonnet 5), nos planos gratuitos, em Python 3. Foram até três tentativas por problema e duas execuções, em 9 e 15 de setembro de 2026, num total de 90 coletas.

## Conteúdo

| Caminho | Conteúdo |
|---|---|
| `coleta_dados_experimento.xlsx` | Planilha original da coleta. A aba **Coleta** tem uma linha por coleta, com vereditos, números das submissões no Beecrowd e observações. |
| `coletas_90.csv` | As 90 coletas em formato aberto, com as métricas de qualidade e as variantes de sensibilidade do Pylint e do índice de manutenibilidade. |
| `tabela_por_problema.csv` | Resultados por problema e ferramenta: aceitações de 0 a 2 e médias das métricas. |
| `mensagens_pylint.csv` | Todas as mensagens do Pylint por arquivo, com a categoria. |
| `prompts/` | Prompt padrão com o enunciado de cada problema e o prompt de correção. |
| `codigos/` | Primeira resposta de cada coleta, no formato `<problema>_<ferramenta>_<execução>.py`. |
| `codigos/correcoes/` | Respostas das tentativas de correção (2ª e 3ª). |
| `codigos/falhas/` | Transcrição da resposta registrada como falha de entrega. |
| `metricas_codigo.py` | Recalcula o Pylint e o Radon sobre os arquivos de `codigos/`. |
| `analise_revisada.py` | Reproduz os testes estatísticos do artigo a partir de `coletas_90.csv`. |

## Como reproduzir

```
pip install pylint radon pandas scipy statsmodels openpyxl
python metricas_codigo.py codigos
python analise_revisada.py
```

## Configuração

- Pylint 4.0.8: `--disable=C0114,C0115,C0116 --module-naming-style=any --disable=C0304`. Escores negativos foram tratados como zero.
- Radon 6.0.1: complexidade ciclomática total do arquivo e índice de manutenibilidade com `multi=True`.
- Unidade de análise: o problema (soma ou média das duas execuções). Correção de Holm para as sete comparações principais.
