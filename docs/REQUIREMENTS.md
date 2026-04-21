📋 Levantamento de Requisitos: Report Automator v2.0

1. Requisitos Funcionais (RF)
📂 Gestão de Arquivos e Configuração

    RF01 - Persistência de Configuração (CRUD TOML): O sistema deve permitir criar, salvar, importar e exportar arquivos .toml de configuração diretamente pela interface.

    RF02 - Ingestão de Arquivos com Cópia de Segurança: Ao selecionar a planilha de origem ou o template, o sistema deve copiar os arquivos para a pasta data/input/. Caso o arquivo já exista, deve realizar a sobrescrita automática.

    RF03 - Localização Dinâmica de Cabeçalho: O usuário deve especificar em qual linha do Excel se iniciam os nomes das colunas (parâmetro header do Pandas).

    RF04 - Persistência de Caminhos (Last Used): O sistema deve lembrar os últimos caminhos de arquivos utilizados para agilizar o uso diário.

⚙️ Extração e Mapeamento Dinâmico

    RF05 - Mapeamento Dinâmico de Categorias (Abas): A interface deve permitir adicionar ou remover dinamicamente quantas abas de origem forem necessárias, mapeando cada uma para uma célula de destino.

    RF06 - Extração Genérica de Colunas: O usuário deve definir uma lista de colunas para extração (ex: Bairro, Serviço, Equipe). O sistema deve buscar essas colunas em todas as abas mapeadas.

    RF07 - Processamento de Metadados de Contrato: O sistema deve calcular automaticamente o cronograma com base na Data Inicial e no Prazo (Dias), gerando a Data Final e o Tempo Decorrido.

    RF08 - Mapeamento de Células de Metadados: O usuário deve definir em quais células do template a Data de Início, Data Final e o Tempo Decorrido devem ser inseridos.

🛠️ Processamento e Saída

    RF09 - Motor ETL com Clonagem de Layout: O sistema deve gerar uma aba para cada dia do mês, clonando integralmente a formatação, fórmulas e imagens do template base.

    RF10 - Formatação de Texto Inteligente: Aplicar lógica de Title Case em colunas dinâmicas, preservando siglas técnicas (LED, RJ, etc.) e preposições em minúsculo.

    RF11 - Log de Eventos em Tempo Real: Console visual com auto-scroll detalhando sucessos, avisos e erros críticos de cada etapa do processamento.

2. Requisitos Não-Funcionais (RNF)

    RNF01 - Arquitetura Assíncrona: O processamento pesado deve rodar em uma QThread separada para evitar o congelamento da interface (GUI).

    RNF02 - Portabilidade Total: O software deve ser empacotado como .exe (Windows) e funcionar de forma portátil (sem instalador), buscando arquivos em pastas relativas.

    RNF03 - Desempenho de E/S: O sistema deve validar a existência e a permissão de escrita (check de arquivo aberto) antes de iniciar o loop de processamento.

    RNF04 - Interface Modular (UX): A GUI deve ser dividida em seções claras: (A) Arquivos, (B) Mapeamento e Contrato, (C) Execução e Logs.

3. Regras de Negócio (RN)

    RN01 - Cálculo de Tempo Decorrido: O tempo decorrido deve ser calculado pela fórmula:
    Dias Decorridos=(Data Atual−Data Inicial)+1

    RN02 - Validação de Arquivo Bloqueado: Se o arquivo de saída estiver aberto no Excel, o sistema deve interromper o processo e alertar o usuário imediatamente através do log.

    RN03 - Consolidação de Valores Únicos: Para cada coluna extraída, o sistema deve remover duplicatas do mesmo dia e aba, unindo-as com um separador configurável (ex: " | ").

    RN04 - Fallback de Recursos: Caso o usuário não forneça um template personalizado em data/input, o sistema deve utilizar o template padrão localizado em assets/.

    RN05 - Integridade de Colunas: Caso uma coluna configurada não exista em uma aba específica, o sistema deve registrar um Warning no log e prosseguir com as demais colunas.
