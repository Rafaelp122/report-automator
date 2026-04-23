import pytest
import os
import tomllib
from src.app.infra.config_manager import ConfigManager
from src.app.core.config_models import ReportConfig, ProjectConfig

class TestConfigManager:
    @pytest.fixture
    def config_file(self, tmp_path):
        path = tmp_path / "config.toml"
        content = b'[projeto]\nnome = "Teste"\nano = 2026\n'
        path.write_bytes(content)
        return str(path)

    def test_load_config_success(self, config_file):
        manager = ConfigManager(config_file)
        config = manager.load_config()
        assert config.projeto.nome == "Teste"
        assert config.projeto.ano == 2026

    def test_load_config_file_not_found(self):
        manager = ConfigManager("non_existent.toml")
        config = manager.load_config()
        assert config.projeto.mes is not None

    def test_save_config(self, tmp_path):
        path = tmp_path / "save_test.toml"
        manager = ConfigManager(str(path))
        new_config = ReportConfig(projeto=ProjectConfig(nome="Salvo"))
        
        manager.save_config(new_config)
        
        with open(path, "rb") as f:
            saved = tomllib.load(f)
        assert saved["projeto"]["nome"] == "Salvo"

    def test_import_config(self, tmp_path):
        source = tmp_path / "source.toml"
        source.write_bytes(b'[projeto]\nnome = "Importado"\n')
        
        manager = ConfigManager()
        imported = manager.import_config(str(source))
        
        assert imported.projeto.nome == "Importado"
        assert manager.config.projeto.nome == "Importado"

    def test_export_config(self, tmp_path):
        target = tmp_path / "export.toml"
        manager = ConfigManager()
        config = ReportConfig(projeto=ProjectConfig(nome="Exportado"))
        
        manager.export_config(str(target), config)
        
        with open(target, "rb") as f:
            exported = tomllib.load(f)
        assert exported["projeto"]["nome"] == "Exportado"
