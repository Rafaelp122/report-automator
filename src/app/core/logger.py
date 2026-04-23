import logging
from src.app.core.constants import APP_LOG_PATH

def setup_logger(name="rdo_automator", log_path=None, level=logging.INFO):
    """Configura o logger principal da aplicação usando caminhos do constants.py."""
    path = log_path or APP_LOG_PATH
    
    # Garante que o diretório de logs existe
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Formato do log: Data - Nome - Nível - Mensagem
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para o console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Handler para o arquivo
    file_handler = logging.FileHandler(str(path), encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Configura o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicidade de handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Instância padrão para o projeto
logger = setup_logger()
