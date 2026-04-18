import pytest
import os
import tomllib
from unittest.mock import MagicMock, patch
from src.app.ui.workers.processor_worker import ProcessorWorker

class TestProcessorWorker:
    
    def test_run_success(self, qtbot, tmp_path, monkeypatch):
        # Setup mock environment
        os.chdir(tmp_path)
        
        # Create a mock config.toml
        config_content = {
            'arquivos': {
                'dados_origem': 'dados.xlsx',
                'default_template': 'default.xlsx',
                'user_template': 'user.xlsx'
            }
        }
        with open("config.toml", "wb") as f:
            import tomli_w
            f.write(tomli_w.dumps(config_content).encode())
            
        # Create dummy files
        (tmp_path / "dados.xlsx").touch()
        (tmp_path / "default.xlsx").touch()
        
        worker = ProcessorWorker()
        
        # Connect signals to monitor them
        with qtbot.waitSignal(worker.finished, timeout=2000) as blocker:
            with patch('src.app.ui.workers.processor_worker.ExcelHandler') as MockHandler:
                mock_handler_inst = MockHandler.return_value
                mock_handler_inst.gerar_diario_completo.return_value = "resultado.xlsx"
                
                worker.run()
                
        assert blocker.args == ["resultado.xlsx"]
        # Should have used default template as user.xlsx doesn't exist
        MockHandler.assert_called_once()
        called_config = MockHandler.call_args[0][0]
        assert called_config['arquivos']['template_ativo'] == 'default.xlsx'

    def test_run_user_template_priority(self, qtbot, tmp_path, monkeypatch):
        os.chdir(tmp_path)
        
        config_content = {
            'arquivos': {
                'dados_origem': 'dados.xlsx',
                'default_template': 'default.xlsx',
                'user_template': 'user.xlsx'
            }
        }
        with open("config.toml", "wb") as f:
            import tomli_w
            f.write(tomli_w.dumps(config_content).encode())
            
        (tmp_path / "dados.xlsx").touch()
        (tmp_path / "default.xlsx").touch()
        (tmp_path / "user.xlsx").touch() # User template exists
        
        worker = ProcessorWorker()
        
        with qtbot.waitSignal(worker.finished, timeout=2000):
            with patch('src.app.ui.workers.processor_worker.ExcelHandler') as MockHandler:
                mock_handler_inst = MockHandler.return_value
                mock_handler_inst.gerar_diario_completo.return_value = "resultado.xlsx"
                worker.run()
                
        called_config = MockHandler.call_args[0][0]
        assert called_config['arquivos']['template_ativo'] == 'user.xlsx'

    def test_run_config_missing(self, qtbot, tmp_path):
        os.chdir(tmp_path)
        # config.toml NOT created
        
        worker = ProcessorWorker()
        
        with qtbot.waitSignal(worker.error, timeout=2000) as blocker:
            worker.run()
            
        assert "config.toml não encontrado" in blocker.args[0]

    def test_run_data_file_missing(self, qtbot, tmp_path):
        os.chdir(tmp_path)
        config_content = {
            'arquivos': {
                'dados_origem': 'missing_data.xlsx',
                'default_template': 'default.xlsx'
            }
        }
        with open("config.toml", "wb") as f:
            import tomli_w
            f.write(tomli_w.dumps(config_content).encode())
            
        worker = ProcessorWorker()
        
        with qtbot.waitSignal(worker.error, timeout=2000) as blocker:
            worker.run()
            
        assert "Arquivo de dados não encontrado" in blocker.args[0]
