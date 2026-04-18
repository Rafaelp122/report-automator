import tomllib
from src.app.core.logger import logger

class ConfigManager:
    """Gerencia a leitura do arquivo config.toml"""
    def __init__(self, config_path="config.toml"):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        try:
            with open(self.config_path, "rb") as f:
                self.config = tomllib.load(f)
            logger.info(f"Configuração carregada com sucesso de: {self.config_path}")
            return self.config
        except Exception as e:
            logger.error(f"Erro ao carregar configuração ({self.config_path}): {e}")
            raise
