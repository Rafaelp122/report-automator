# 🗺️ Esquema de Configuração: config.toml (v2.0)

Este documento define a estrutura e a inteligência de dados do arquivo `config.toml`.

## 1. Seção [extração] - Inteligência Gramatical
Esta seção define como os dados são coletados e transformados em frases naturais.

- `colunas` (lista): Lista de colunas para extração (ex: `["Serviço", "Bairro"]`).
- `separador_lista` (string): Usado entre itens (padrão: `", "`).
- `conector_final` (string): Usado antes do último item (padrão: `" e "`).
- `formato_final` (string): Template com suporte a **Pluralização Dinâmica**.

### Regras de Pluralização no Template:
O sistema busca marcadores de plural associados às chaves de extração:
- `{Chave:s}`: Adiciona "s" se houver +1 item.
- `{Chave:es}`: Adiciona "es" se houver +1 item.
- `{Chave:nos}`: Transforma "No" em "Nos" ou "Na" em "Nas" se houver +1 item.

**Exemplo de Template:**
`"{Serviço:nos} serviço{Serviço:s} realizado{Serviço:s}: {Serviço}. {Bairro:nos} bairro{Bairro:s}: {Bairro}."`

---

## 2. Exemplo de Configuração Completa

```toml
[projeto]
nome = "Relatório de Manutenção"
mes = 2
ano = 2026

[arquivos]
linha_cabecalho = 4
dados_origem = "data/input/dados.xlsx"
user_template = "data/input/template.xlsx"

[contrato]
data_inicio = "2026-01-01"
prazo_dias = 365

[extração]
colunas = ["Serviço", "Bairro"]
separador_lista = ", "
conector_final = " e "
formato_final = "{Serviço:nos} serviço{Serviço:s} realizado{Serviço:s}: {Serviço}. {Bairro:nos} bairro{Bairro:s}: {Bairro}."

[posicoes]
celula_data_atual = "E3"
celula_tempo_decorrido = "R11"
# ... demais coordenadas

[mapeamento]
Manual = "B15"
Mecanica = "B20"
```
