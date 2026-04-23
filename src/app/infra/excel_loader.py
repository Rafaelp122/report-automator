import pandas as pd
from typing import Dict
from src.app.core.logger import logger

class ExcelLoader:
    """Responsável por carregar e pré-processar dados do Excel de origem"""
    
    def __init__(self, file_path: str, header_row: int = 0):
        self.file_path = file_path
        self.header_row = header_row

    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """Carrega todas as abas e normaliza as colunas de data"""
        logger.info(f"Lendo dados de: {self.file_path} (header na linha {self.header_row})")
        
        try:
            abas = pd.read_excel(self.file_path, sheet_name=None, header=self.header_row)
            return self._normalize_dates(abas)
        except Exception as e:
            logger.error(f"Erro ao carregar Excel de origem: {e}")
            raise

    def _normalize_dates(self, abas: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Normaliza as colunas de data uma única vez para todas as abas"""
        for nome_aba, df in abas.items():
            col_data = self._find_date_column(df)
            if col_data:
                df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
                # Adicionamos uma coluna auxiliar de dia para otimizar a busca no loop principal
                df['_dia_aux'] = df[col_data].dt.day
            else:
                df['_dia_aux'] = None
        return abas

    @staticmethod
    def _find_date_column(df: pd.DataFrame) -> str:
        """Localiza a coluna que contém informações de data"""
        for col in df.columns:
            if 'data' in str(col).lower():
                return col
        return ""
