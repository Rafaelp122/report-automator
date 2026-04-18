import os
import tomllib
from PySide6.QtCore import QObject, Signal, Slot
from src.app.infra.excel_handler import ExcelHandler

class ProcessorWorker(QObject):
    """
    Worker class to handle Excel processing in a background thread.
    Keeps the UI logic clean and decoupled.
    """
    progress_log = Signal(str)
    finished = Signal(str)
    error = Signal(str)

    @Slot()
    def run(self):
        try:
            self.progress_log.emit("Lendo configurações...")
            if not os.path.exists("config.toml"):
                raise FileNotFoundError("config.toml não encontrado.")

            with open("config.toml", "rb") as f:
                config = tomllib.load(f)

            self.progress_log.emit("Validando arquivos...")
            if not os.path.exists(config['arquivos']['dados_origem']):
                raise FileNotFoundError(f"Arquivo de dados não encontrado: {config['arquivos']['dados_origem']}")
            
            # Lógica de Prioridade de Template
            user_tmpl = config['arquivos'].get('user_template')
            default_tmpl = config['arquivos'].get('default_template')
            
            if user_tmpl and os.path.exists(user_tmpl):
                self.progress_log.emit(f"Usando template customizado: {user_tmpl}")
                config['arquivos']['template_ativo'] = user_tmpl
            else:
                self.progress_log.emit("Usando template padrão do sistema.")
                config['arquivos']['template_ativo'] = default_tmpl

            self.progress_log.emit("Gerando abas diárias...")
            handler = ExcelHandler(config)
            arquivo_final = handler.gerar_diario_completo()
            
            self.progress_log.emit(f"Concluído: {arquivo_final}")
            self.finished.emit(arquivo_final)
            
        except Exception as e:
            self.progress_log.emit(f"FALHA: {str(e)}")
            self.error.emit(str(e))
