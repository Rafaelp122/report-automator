# 🏗️ Fluxo do Sistema: Report Automator v2.0

Este documento detalha o ciclo de vida da aplicação, desde a inicialização até a entrega do relatório final, incluindo as novas lógicas de metadados e validação.

---

## 🏗️ Fase 1: Inicialização e Carregamento

Logo ao abrir o executável no Windows:

1.  **Bootstrapping**: O `main.py` inicia a `QApplication` e carrega o arquivo de estilos `main.qss`.
2.  **Leitura do Estado**: O sistema busca o arquivo `config.toml` na raiz.
    *   Se existir, preenche o formulário automaticamente com os últimos caminhos e mapeamentos.
    *   Se não existir, carrega um "Estado Zero" (campos vazios).
3.  **Montagem da UI**: A `MainWindow` renderiza as três seções: (A) Arquivos, (B) Configuração e Mapeamento, (C) Execução e Logs.

---

## 📥 Fase 2: Ingestão de Dados e Configuração

O usuário interage com a interface para preparar o "terreno":

1.  **Seleção de Arquivos**: O usuário seleciona a Planilha de Dados e o Template Excel.
2.  **Cópia de Segurança**: Assim que selecionados, o sistema executa `shutil.copy2()`, movendo esses arquivos para `data/input/`. O log avisa: *"Arquivo medicao.xlsx importado para o ambiente local."*
3.  **Dados do Contrato**: O usuário preenche a seção de metadados:
    *   **Data Inicial**: (QDateEdit) + Célula de destino (ex: R8).
    *   **Prazo (Dias)**: (QSpinBox) + Célula de destino (ex: R9).
4.  **Cálculos Automáticos**: O sistema exibe/mapeia as células para:
    *   **Data Final**: (Célula ex: R10).
    *   **Data Atual (Aba)**: (Célula ex: E3).
    *   **Tempo Decorrido**: (Célula ex: R11).
5.  **Mapeamento de Abas e Colunas**: 
    *   O usuário adiciona linhas na tabela de mapeamento (ex: `manual -> B15`).
    *   O usuário define as colunas dinâmicas para extração (ex: Bairro, Serviço).

---

## 🔍 Fase 3: Validação Pré-Voo

O `ValidationWorker` atua em uma thread secundária:

1.  **Check de Estrutura**: O Pandas verifica se as abas e colunas configuradas existem na planilha de origem.
2.  **Check de Bloqueio**: O sistema verifica se o arquivo de saída em `data/output/` está aberto. Se estiver, o erro crítico é exibido: *"Ação bloqueada: Feche o arquivo antes de continuar."*
3.  **Validação de Metadados**:
    *   **Formato de Célula**: Verifica se as coordenadas seguem o padrão Excel (ex: AA100).
    *   **Cálculo Preventivo**: Alerta se a data do mês atual for anterior à data de início do contrato.
    *   **Check de Sobreposição**: Garante que células de metadados não coincidam com células de serviços.

---

## ⚙️ Fase 4: O Motor de Processamento (ETL)

Ao clicar em **[GERAR DIÁRIO DE OBRA]**, o `ProcessorWorker` assume o controle em loop diário (01 a 31):

1.  **Clonagem**: O `openpyxl` cria uma cópia exata da aba `template.xlsx` para cada dia.
2.  **Inserção de Metadados**:
    *   **Dados Fixos**: Escreve Data de Início, Data Final e Prazo nas células mapeadas.
    *   **Dados Dinâmicos**: Escreve a Data Atual da aba.
    *   **Tempo Decorrido**: Calculado como `(Data Atual - Data Início) + 1`.
3.  **Extração de Colunas**:
    *   Filtra o DataFrame para o dia e aba correspondente.
    *   Remove nulos e duplicatas.
    *   Aplica o `TextProcessor` (Title Case e Siglas).
4.  **Escrita Consolidada**: Injeta o texto final (ex: *"Bairro: Centro | Serviço: Poda"*) na célula de destino.
5.  **Progresso**: Envia sinais para atualizar a barra de progresso da UI.

---

## 🏁 Fase 5: Finalização e Entrega

1.  **Limpeza**: Remove a aba original de "exemplo" do template clonado.
2.  **Salvamento**: Grava o arquivo final em `data/output/` com nome formatado.
3.  **Feedback**: Exibe `QMessageBox` de sucesso e resumo no Log.
4.  **Ação de Saída**: Habilita o botão "Abrir Pasta de Saída".

---

## 🛠️ Especificações Técnicas Adicionais

### Estrutura do config.toml
```toml
[contrato]
data_inicio = "2026-01-01"
prazo_dias = 365

[posicoes]
celula_data_inicio = "R8"
celula_prazo_dias = "R9"
celula_data_final = "R10"
celula_data_atual = "E3"
celula_tempo_decorrido = "R11"

[mapeamento]
manual = "B15"
mecanica = "B20"
```

### Lógica de Cálculo (Python)
```python
delta = data_atual - data_inicio
tempo_decorrido = delta.days + 1
nova_ws[pos['celula_tempo_decorrido']] = f"{tempo_decorrido} dias"
```
