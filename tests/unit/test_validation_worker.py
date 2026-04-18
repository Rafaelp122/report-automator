import pytest
import os
import tomli_w
from src.app.ui.workers.validation_worker import ValidationWorker

class TestValidationWorker:
    
    def test_coordinate_validation_logic(self):
        worker = ValidationWorker()
        assert worker.is_valid_excel_coordinate("A1") is True
        assert worker.is_valid_excel_coordinate("Z99") is True
        assert worker.is_valid_excel_coordinate("ABC1000") is True
        assert worker.is_valid_excel_coordinate("A0") is False
        assert worker.is_valid_excel_coordinate("1A") is False
        assert worker.is_valid_excel_coordinate("A") is False
        assert worker.is_valid_excel_coordinate("ZZZZ1") is False # Max 3 letters (XFD is max in Excel, but 3 is a good limit)

    def test_run_validation_invalid_coordinate(self, qtbot, tmp_path):
        os.chdir(tmp_path)
        config_content = {
            'arquivos': {
                'dados_origem': 'dados.xlsx',
            },
            'posicoes': {
                'celula_data': 'INVALID'
            },
            'mapeamento': {
                'teste': 'B10'
            },
            'colunas': {
                'data': 'Data',
                'servico': 'Servico'
            }
        }
        with open("config.toml", "wb") as f:
            f.write(tomli_w.dumps(config_content).encode())
            
        (tmp_path / "dados.xlsx").touch()
        
        worker = ValidationWorker()
        with qtbot.waitSignal(worker.validation_finished, timeout=2000) as blocker:
            worker.run()
            
        sucesso, erros = blocker.args
        assert sucesso is False
        assert any("Célula da data 'INVALID' é inválida" in e for e in erros)
