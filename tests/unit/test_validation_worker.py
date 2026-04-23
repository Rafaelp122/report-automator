import pytest
from src.app.ui.workers.validation_worker import ValidationWorker
from src.app.core.validator import ReportValidator
from src.app.core.config_models import ReportConfig, FilesConfig, PositionsConfig, ExtractionConfig

class TestValidationWorker:
    
    def test_coordinate_validation_logic(self):
        validator = ReportValidator()
        assert validator.is_valid_excel_coordinate("A1") is True
        assert validator.is_valid_excel_coordinate("Z99") is True
        assert validator.is_valid_excel_coordinate("ABC1000") is True
        assert validator.is_valid_excel_coordinate("A0") is False
        assert validator.is_valid_excel_coordinate("1A") is False
        assert validator.is_valid_excel_coordinate("A") is False
        assert validator.is_valid_excel_coordinate("ZZZZ1") is False

    def test_run_validation_invalid_coordinate(self, qtbot, tmp_path):
        dados_path = tmp_path / "dados.xlsx"
        dados_path.touch()
        
        config = ReportConfig(
            arquivos=FilesConfig(dados_origem=str(dados_path)),
            posicoes=PositionsConfig(celula_data_atual='INVALID'),
            extracao=ExtractionConfig(colunas=['Data', 'Servico']),
            mapeamento={'teste': 'B10'}
        )
            
        validator = ReportValidator()
        worker = ValidationWorker(config, validator)
        
        with qtbot.waitSignal(worker.validation_finished, timeout=2000) as blocker:
            worker.run()
            
        sucesso, erros, field_errors = blocker.args
        assert sucesso is False
        assert any("Célula" in e and "inválida" in e for e in erros)
        assert "celula_data_atual" in field_errors
