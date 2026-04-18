import time
from PySide6.QtCore import QObject, Signal, Slot
from src.app.core.logger import logger
from src.app.core.validator import ReportValidator
from src.app.infra.config_manager import ConfigManager

class ValidationWorker(QObject):
    """
    Worker para validar a integridade dos dados e mapeamentos.
    Atua como ponte entre a UI e o ReportValidator (Core).
    """
    progress_log = Signal(str)
    validation_finished = Signal(bool, list)
    finished = Signal()

    @Slot()
    def run(self):
        try:
            msg = "Iniciando validação de mapeamento..."
            logger.info(msg)
            self.progress_log.emit(msg)
            time.sleep(0.3)
            
            # Carregar Configurações usando o ConfigManager
            config_manager = ConfigManager()
            config = config_manager.load_config()

            # Delegar validação para o Core
            validator = ReportValidator()
            sucesso, erros = validator.validate(config)

            for erro in erros:
                self.progress_log.emit(f"ERRO: {erro}")

            if sucesso:
                msg = "Tudo ok! Mapeamento validado."
                logger.info(msg)
                self.progress_log.emit(msg)
                self.validation_finished.emit(True, [])
            else:
                logger.warning(f"Validação concluída com {len(erros)} erros.")
                self.validation_finished.emit(False, erros)

        except Exception as e:
            err_msg = f"Erro fatal na validação: {str(e)}"
            logger.exception(err_msg)
            self.progress_log.emit(err_msg)
            self.validation_finished.emit(False, [str(e)])
        
        finally:
            self.finished.emit()
