import logging
import os
from datetime import datetime

def setup_logger(name="report_automator", log_file="app.log", level=logging.INFO):
    """Configura o logger principal da aplicação."""
    
    # Cria o diretório de logs se não existir
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_path = os.path.join(log_dir, log_file)
    
    # Formato do log: Data - Nome - Nível - Mensagem
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para o console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Handler para o arquivo (rotativo simples com data no nome ou apenas um arquivo fixo)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Configura o logger raiz ou um específico
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicidade de handlers se a função for chamada múltiplas vezes
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Instância padrão para o projeto
logger = setup_logger()
