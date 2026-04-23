import re
import pandas as pd
from pathlib import Path
from src.app.core.logger import logger
from src.app.core.config_models import ReportConfig

class ReportValidator:
    """
    Serviço core para validar a integridade dos dados e mapeamentos.
    Desacoplado da interface gráfica e usando o modelo ReportConfig.
    """

    @staticmethod
    def is_valid_excel_coordinate(coord: str) -> bool:
        """Valida se uma string é uma coordenada Excel válida (ex: A1, B10, Z100)"""
        return bool(re.match(r'^[A-Z]{1,3}[1-9][0-9]*$', str(coord).upper()))

    def validate(self, config: ReportConfig) -> tuple[bool, list[str], dict[str, str]]:
        """
        Executa a validação completa baseada no modelo ReportConfig.
        Retorna (sucesso: bool, erros_log: list[str], field_errors: dict[str, str])
        """
        erros_log = []
        field_errors = {}
        
        # 1. Validar Coordenadas de Posições Fixas
        posicoes = config.posicoes.model_dump()
        for nome_pos, celula in posicoes.items():
            if celula and not self.is_valid_excel_coordinate(celula):
                msg = f"Célula '{celula}' para '{nome_pos}' é inválida."
                erros_log.append(msg)
                field_errors[nome_pos] = msg

        # 2. Validar Extração e Formato Final
        ext = config.extracao
        tags_no_formato = re.findall(r'\{([^}:]+)(?::[^}]+)?\}', ext.formato_final)
        for tag in tags_no_formato:
            if tag not in ext.colunas:
                msg = f"A tag '{{{tag}}}' no formato final não está nas colunas selecionadas."
                erros_log.append(msg)
                field_errors["formato_final"] = msg

        # 3. Verificar Arquivo de Origem
        origem = Path(config.arquivos.dados_origem)
        if not origem.exists() or config.arquivos.dados_origem == "":
            msg = f"Arquivo de origem não encontrado: {origem}"
            erros_log.append(msg)
            field_errors["dados_origem"] = msg
            return False, erros_log, field_errors

        # 4. Validar Abas e Colunas no Excel
        try:
            with pd.ExcelFile(origem) as xls:
                abas_no_arquivo = xls.sheet_names
                header = config.arquivos.linha_cabecalho
                
                for nome_aba, celula in config.mapeamento.items():
                    if not self.is_valid_excel_coordinate(celula):
                        msg = f"Célula de destino '{celula}' para aba '{nome_aba}' é inválida."
                        erros_log.append(msg)
                        field_errors[f"mapeamento_{nome_aba}"] = msg

                    if nome_aba not in abas_no_arquivo:
                        msg = f"Aba '{nome_aba}' não encontrada no arquivo de origem."
                        erros_log.append(msg)
                        field_errors[f"mapeamento_{nome_aba}"] = msg
                        continue
                    
                    # Verificar se colunas esperadas existem na aba
                    df_header = pd.read_excel(xls, sheet_name=nome_aba, header=header, nrows=0)
                    for col in ext.colunas:
                        if col not in df_header.columns:
                            msg = f"Aba '{nome_aba}': Coluna '{col}' não encontrada."
                            erros_log.append(msg)
                            field_errors["colunas"] = msg
                            field_errors[f"mapeamento_{nome_aba}"] = msg
                            
        except Exception as e:
            msg = f"Erro ao ler arquivo Excel: {e}"
            erros_log.append(msg)
            field_errors["dados_origem"] = msg

        return (len(erros_log) == 0), erros_log, field_errors
