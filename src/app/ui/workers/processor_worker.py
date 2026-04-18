from PySide6.QtCore import QObject, Signal, Slot
from src.app.core.logger import logger
from src.app.core.report_service import ReportService
from src.app.infra.config_manager import ConfigManager

class ProcessorWorker(QObject):
    """
    Worker para processamento Excel em segundo plano.
    Atua como ponte entre a UI e o ReportService (Core).
    """
    progress_log = Signal(str)
    progress_update = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    @Slot()
    def run(self):
        try:
            self.progress_log.emit("Carregando configurações...")
            config_manager = ConfigManager()
            config = config_manager.load_config()

            self.progress_log.emit("Iniciando serviço de relatório...")
            service = ReportService()
            
            arquivo_final = service.generate_report(
                config, 
                progress_callback=self.progress_update.emit
            )
            
            self.progress_log.emit(f"Relatório gerado com sucesso: {arquivo_final}")
            self.finished.emit(arquivo_final)
            
        except Exception as e:
            err_msg = f"FALHA: {str(e)}"
            logger.exception(err_msg)
            self.progress_log.emit(err_msg)
            self.error.emit(str(e))
