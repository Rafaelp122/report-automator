from pathlib import Path
from src.app.core.logger import logger
from src.app.core.report_builder import ReportBuilder
from src.app.core.config_models import ReportConfig
from src.app.core.constants import OUTPUT_DIR, DEFAULT_TEMPLATE_PATH

class ReportService:
    """
    Serviço de Domínio para orquestrar a geração de relatórios.
    Faz a ponte entre a configuração validada e o ReportBuilder.
    """

    def generate_report(self, config: ReportConfig, progress_callback=None) -> str:
        """Orquestra o fluxo completo de geração do relatório"""
        
        # 1. Validar e definir caminhos (Usando Pathlib)
        origem = Path(config.arquivos.dados_origem)
        if not origem.exists():
            raise FileNotFoundError(f"Arquivo de origem não encontrado: {origem}")
        
        # 2. Lógica de Prioridade de Template
        user_tmpl = Path(config.arquivos.user_template) if config.arquivos.user_template else None
        
        if user_tmpl and user_tmpl.exists():
            logger.info(f"Usando template customizado: {user_tmpl}")
            config.arquivos.template_ativo = str(user_tmpl)
        else:
            if not DEFAULT_TEMPLATE_PATH.exists():
                raise FileNotFoundError(f"Template padrão não encontrado: {DEFAULT_TEMPLATE_PATH}")
            logger.info("Usando template padrão do sistema.")
            config.arquivos.template_ativo = str(DEFAULT_TEMPLATE_PATH)

        # 3. Definir nome do arquivo de saída
        nome_saida = f"Diario_Consolidado_{config.projeto.mes:02d}_{config.projeto.ano}.xlsx"
        caminho_saida = OUTPUT_DIR / nome_saida

        # 4. Delegar para o ReportBuilder
        builder = ReportBuilder(config)
        arquivo_final = builder.build(caminho_saida, progress_callback=progress_callback)
        
        return str(arquivo_final)
