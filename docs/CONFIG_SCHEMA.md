# 🗺️ Esquema de Configuração: config.toml (v1.0)

Este documento define a estrutura, os tipos de dados e a inteligência por trás do arquivo `config.toml`.

## 1. Regras Gerais
- **Padrão de Datas**: Todas as datas armazenadas no TOML devem seguir obrigatoriamente o padrão ISO **`YYYY-MM-DD`** (ex: `2026-01-01`). Isso garante compatibilidade universal e evita erros de conversão regional.
- **Caminhos**: Devem ser preferencialmente relativos à raiz do projeto (ex: `data/input/arquivo.xlsx`).

---

## 2. Descrição das Seções

### [projeto]
- `nome` (string): Nome do projeto ou cliente.
- `mes` (integer): Mês de referência do relatório (1-12).
- `ano` (integer): Ano de referência (ex: 2026).

### [arquivos]
- `linha_cabecalho` (integer): Linha do Excel onde se encontra o cabeçalho (0-indexed).
- `dados_origem` (string): Caminho do arquivo de dados bruto.
- `user_template` (string): Caminho do template personalizado.

### [contrato]
- `data_inicio` (string): Data inicial do contrato (**`YYYY-MM-DD`**).
- `prazo_dias` (integer): Prazo total de execução em dias.

### [extração] - Inteligência Gramatical
- `colunas` (lista): Colunas a serem extraídas do Excel.
- `separador_lista` (string): Separador entre itens da lista (ex: `", "`).
- `conector_final` (string): Conector para o último item (ex: `" e "`).
- `formato_final` (string): Template com suporte a pluralização:
    - `{Chave:s}`: Plural "s".
    - `{Chave:es}`: Plural "es".
    - `{Chave:nos}`: "No" -> "Nos" / "Na" -> "Nas".

### [posicoes] (Coordenadas Excel)
- `celula_data_inicio`: Destino da Data Inicial.
- `celula_prazo_dias`: Destino do Prazo.
- `celula_data_final`: Destino da Data Final calculada.
- `celula_data_atual`: Destino da Data da Aba (ex: `E3`).
- `celula_tempo_decorrido`: Destino do tempo decorrido calculado.

### [mapeamento]
- Dicionário dinâmico relacionando `Nome da Aba` -> `Célula de Destino`.

---

## 3. Exemplo de Configuração Completa

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
celula_data_inicio = "R8"
celula_prazo_dias = "R9"
celula_data_final = "R10"
celula_data_atual = "E3"
celula_tempo_decorrido = "R11"

[mapeamento]
Manual = "B15"
Mecanica = "B20"
```
