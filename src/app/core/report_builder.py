import calendar
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
from src.app.core.logger import logger
from src.app.core.processor import TextProcessor
from src.app.core.config_models import ReportConfig
from src.app.infra.excel_loader import ExcelLoader
from src.app.infra.template_manager import TemplateManager

class ReportBuilder:
    """Orquestrador principal para construção do relatório consolidado"""
    
    def __init__(self, config: ReportConfig):
        self.config = config

    def build(self, output_path: Path, progress_callback=None) -> Path:
        """Executa o loop de construção do diário"""
        # 1. Carregar Dados de Origem
        loader = ExcelLoader(
            self.config.arquivos.dados_origem, 
            self.config.arquivos.linha_cabecalho
        )
        abas_origem = loader.load_all_sheets()
        
        # 2. Preparar Template
        tm = TemplateManager(self.config.arquivos.template_ativo)
        tm.load()
        
        # 3. Metadados do Período
        ano = self.config.projeto.ano
        mes = self.config.projeto.mes
        _, ultimo_dia = calendar.monthrange(ano, mes)
        
        # Datas do Contrato
        data_inicio = datetime.strptime(self.config.contrato.data_inicio, '%Y-%m-%d')
        prazo_dias = self.config.contrato.prazo_dias
        data_final = data_inicio + timedelta(days=prazo_dias)

        # 4. Loop Diário
        logger.info(f"Iniciando loop diário para {mes}/{ano} ({ultimo_dia} dias)")
        
        for dia in range(1, ultimo_dia + 1):
            if progress_callback:
                progress_callback(int((dia / ultimo_dia) * 100))

            data_atual = datetime(ano, mes, dia)
            ws = tm.clone_worksheet(data_atual.strftime('%d-%m'))
            
            # Preencher Posições Fixas
            self._fill_fixed_positions(ws, data_atual, data_inicio, data_final, prazo_dias)
            
            # Preencher Mapeamentos Dinâmicos
            self._fill_dynamic_mappings(ws, abas_origem, dia)

        # 5. Finalizar e Salvar
        tm.save(output_path)
        return output_path

    def _fill_fixed_positions(self, ws, data_atual, data_inicio, data_final, prazo_dias):
        pos = self.config.posicoes
        if pos.celula_data_inicio:
            ws[pos.celula_data_inicio] = data_inicio.strftime('%d/%m/%Y')
        if pos.celula_prazo_dias:
            ws[pos.celula_prazo_dias] = f"{prazo_dias} dias"
        if pos.celula_data_final:
            ws[pos.celula_data_final] = data_final.strftime('%d/%m/%Y')
        if pos.celula_data_atual:
            ws[pos.celula_data_atual] = data_atual.strftime('%d/%m/%Y')
        if pos.celula_tempo_decorrido:
            delta = data_atual - data_inicio
            ws[pos.celula_tempo_decorrido] = f"{delta.days + 1} dias"

    def _fill_dynamic_mappings(self, ws, abas_origem, dia):
        ext = self.config.extracao
        for nome_aba, celula in self.config.mapeamento.items():
            if nome_aba not in abas_origem:
                ws[celula] = None
                continue
            
            df = abas_origem[nome_aba]
            # OTIMIZAÇÃO: Usando a coluna auxiliar _dia_aux criada no DataLoader
            filtro = df[df['_dia_aux'] == dia]
            
            if not filtro.empty:
                dados_extraidos = {}
                for col in ext.colunas:
                    if col in filtro.columns:
                        dados_extraidos[col] = filtro[col].dropna().unique().tolist()
                
                resumo = TextProcessor.formatar_resumo(
                    dados_extraidos, ext.formato_final, 
                    ext.separador_lista, ext.conector_final
                )
                ws[celula] = resumo
            else:
                ws[celula] = None
