# 🎨 Especificação de UI/UX: Report Automator v2.0

Este documento define a identidade visual, a arquitetura de interface e a experiência do usuário para a evolução do sistema.

---

## 1. Identidade Visual (Look & Feel)

### Paleta de Cores
- **Primária**: Roxo Real (`#3F51B5`) - Botões de ação, cabeçalhos, progresso e estados ativos.
- **Fundo**: Cinza de Superfície (`#F7F9FC`) - Cor da janela principal para reduzir fadiga ocular.
- **Cards**: Branco (`#FFFFFF`) - Seções de formulário com bordas suaves (`border-radius: 12px`).
- **Texto**: Azul Grafite (`#1E293B`) - Alta legibilidade e contraste.
- **Sucesso/Erro**: Verde Esmeralda (`#10B981`) e Vermelho Coral (`#EF4444`).

### Tipografia
- **Interface**: *Inter* ou *Segoe UI* (limpa e moderna).
- **Logs/Console**: *JetBrains Mono* ou *Fira Code* (monospace para legibilidade técnica).

---

## 2. Arquitetura do Layout (Sidebar Navigation)

O sistema adotará um layout de **Sidebar Lateral** para organizar o volume crescente de configurações.

### ⬅️ Painel Lateral (Sidebar)
- **Logotipo**: Ícone estilizado de planilha com engrenagem.
- **Menu de Navegação**:
    1. **Início/Arquivos** (Ícone: Pasta) - Seleção e ingestão.
    2. **Contrato & Metadados** (Ícone: Calendário) - Prazos e coordenadas.
    3. **Mapeamento de Abas** (Ícone: Tabela) - Relação Aba -> Célula.
    4. **Colunas de Extração** (Ícone: Filtro) - Colunas e formato final.
- **Indicadores de Status (Sugestão)**:
    - Cada item do menu terá um indicador visual lateral:
        - ⚪ *Cinza*: Pendente/Vazio.
        - ⚠️ *Amarelo*: Erro de validação.
        - ✅ *Verde*: Validado e pronto.
- **Rodapé**: Botões compactos de [Importar TOML] e [Exportar TOML].

---

## 3. Detalhamento das Seções

### Seção A: Gestão de Arquivos (Cards de Drop)
- Substituição de campos simples por **Cards Interativos**.
- Suporte a *Drag & Drop* direto no card.
- Feedback visual de "Arquivo Importado" com ícone de check após o processamento do `shutil.copy2`.

### Seção B: Metadados do Contrato
- Grid de 2 colunas:
    - **Esquerda**: Seletores de data (`QDateEdit`) e prazo (`QSpinBox`).
    - **Direita**: Inputs de coordenadas (ex: `[ R8 ]`) com prefixo visual "Célula:".
- **Validação On-the-fly**: Bordas vermelhas instantâneas para coordenadas Excel inválidas.

### Seção C: Extração com Chips (Tags)
- O campo "Colunas para Extração" converterá entradas em **Chips/Tags** azuis.
- Permite remoção rápida com um "x" e evita strings longas ilegíveis.

---

## 4. Fluxo de Execução e Feedback

### Painel de Controle (Rodapé Fixo)
- **Barra de Progresso**: Estilo "progressivo suave" com texto dinâmico (ex: *"Processando Dia 12 de 31..."*).
- **Botão de Ação [GERAR DIÁRIO]**:
    - Grande, roxo e centralizado.
    - Transição para estado "Rodando" com spinner de carregamento.

### Console de Logs (Gaveta Retrátil)
- Área expansível na base da janela com logs coloridos:
    - `[ERRO]` em Vermelho.
    - `[AVISO]` em Amarelo.
    - `[OK]` em Verde.

---

## 5. Delighters (Interações Inteligentes)

- **Auto-Save**: Salvamento automático no `config.toml` ao perder o foco do campo (`on blur`).
- **Tooltips Contextuais**: Explicações rápidas sobre fórmulas (ex: Cálculo do Tempo Decorrido).
- **Ações Pós-Sucesso**: Botões rápidos para `[📁 Abrir Pasta]` e `[📊 Abrir Excel]`.
