import os
from openpyxl import load_workbook
from pathlib import Path
from src.app.core.logger import logger

class TemplateManager:
    """Responsável por carregar, clonar e salvar o template Excel"""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.wb = None
        self.ws_template = None

    def load(self):
        """Carrega o workbook e identifica a aba base"""
        if not self.template_path.exists() or self.template_path.stat().st_size == 0:
            raise FileNotFoundError(f"Template inválido ou inexistente: {self.template_path}")
        
        try:
            self.wb = load_workbook(str(self.template_path))
            self.ws_template = self.wb.active
        except Exception as e:
            logger.exception("Erro ao abrir template Excel")
            raise ValueError(f"O arquivo de template não é um Excel (.xlsx) válido: {e}")

    def clone_worksheet(self, title: str):
        """Cria uma nova aba baseada no template"""
        new_ws = self.wb.copy_worksheet(self.ws_template)
        new_ws.title = title
        return new_ws

    def save(self, output_path: Path):
        """Remove a aba base e salva o arquivo final"""
        if self.ws_template:
            self.wb.remove(self.ws_template)
            
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Verifica bloqueio do arquivo
        if output_path.exists():
            try:
                output_path.rename(output_path)
            except OSError:
                raise PermissionError(
                    f"O arquivo '{output_path.name}' está aberto. Por favor, feche-o antes de continuar."
                )

        try:
            self.wb.save(str(output_path))
            logger.info(f"Relatório salvo com sucesso em: {output_path}")
        except Exception as e:
            logger.exception(f"Erro ao salvar arquivo final: {e}")
            raise
