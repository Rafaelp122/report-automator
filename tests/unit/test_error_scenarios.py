import pytest
import os
import pandas as pd
from unittest.mock import MagicMock, patch
from src.app.ui.workers.validation_worker import ValidationWorker
from src.app.core.validator import ReportValidator
from src.app.core.report_builder import ReportBuilder
from src.app.core.config_models import ReportConfig, FilesConfig, PositionsConfig, ExtractionConfig

class TestValidationScenarios:
    
    def test_validation_missing_origin_file(self, qtbot, tmp_path):
        config = ReportConfig(
            arquivos=FilesConfig(dados_origem='non_existent.xlsx'),
            posicoes=PositionsConfig(celula_data_atual='E3'),
            mapeamento={'aba1': 'B10'},
            extracao=ExtractionConfig(colunas=['Data', 'Servico'])
        )
            
        validator = ReportValidator()
        worker = ValidationWorker(config, validator)
        with qtbot.waitSignal(worker.validation_finished, timeout=2000) as blocker:
            worker.run()
        
        sucesso, erros, field_errors = blocker.args
        assert sucesso is False
        assert any("Arquivo de origem não encontrado" in e for e in erros)

    def test_validation_missing_sheet(self, qtbot, tmp_path):
        # Create excel with only 'Sheet1'
        data_path = tmp_path / "data.xlsx"
        pd.DataFrame({'Data': [1], 'Servico': [1]}).to_excel(data_path, sheet_name='Sheet1', index=False)
        
        config = ReportConfig(
            arquivos=FilesConfig(dados_origem=str(data_path)),
            posicoes=PositionsConfig(celula_data_atual='E3'),
            mapeamento={'AbaInexistente': 'B10'},
            extracao=ExtractionConfig(colunas=['Data', 'Servico'])
        )
            
        validator = ReportValidator()
        worker = ValidationWorker(config, validator)
        with qtbot.waitSignal(worker.validation_finished, timeout=2000) as blocker:
            worker.run()
        
        sucesso, erros, field_errors = blocker.args
        assert sucesso is False
        assert any("Aba 'AbaInexistente' não encontrada" in e for e in erros)

    def test_validation_missing_column(self, qtbot, tmp_path):
        data_path = tmp_path / "data.xlsx"
        pd.DataFrame({'Data': [1]}).to_excel(data_path, sheet_name='Aba1', index=False) # Missing 'Servico'
        
        config = ReportConfig(
            arquivos=FilesConfig(dados_origem=str(data_path)),
            posicoes=PositionsConfig(celula_data_atual='E3'),
            mapeamento={'Aba1': 'B10'},
            extracao=ExtractionConfig(colunas=['Data', 'Servico'])
        )
            
        validator = ReportValidator()
        worker = ValidationWorker(config, validator)
        with qtbot.waitSignal(worker.validation_finished, timeout=2000) as blocker:
            worker.run()
        
        sucesso, erros, field_errors = blocker.args
        assert sucesso is False
        assert any("Coluna 'Servico' não encontrada" in e for e in erros)

class TestReportBuilderErrorScenarios:
    
    def test_file_locked_error(self, tmp_path):
        # Setup data and template
        data_path = tmp_path / "data.xlsx"
        # We need a dummy excel file for loader
        pd.DataFrame({'Data': [pd.Timestamp('2026-03-01')], 'Servico': ['S1']}).to_excel(data_path, index=False, sheet_name='aba1')
        
        from openpyxl import Workbook
        template_path = tmp_path / "template.xlsx"
        wb = Workbook()
        wb.save(template_path)
        
        config = ReportConfig(
            projeto={'ano': 2026, 'mes': 3},
            arquivos={
                'dados_origem': str(data_path),
                'template_ativo': str(template_path)
            },
            posicoes={'celula_data_atual': 'A1'},
            extracao={'colunas': ['Data', 'Servico']},
            mapeamento={'aba1': 'B1'}
        )
        
        output_path = tmp_path / "output.xlsx"
        output_path.touch()
        
        builder = ReportBuilder(config)
        
        # Simular que o arquivo está aberto forçando um OSError no Path.rename
        with patch('pathlib.Path.rename') as mock_rename:
            mock_rename.side_effect = OSError("File locked")
            with pytest.raises(PermissionError, match="está aberto. Por favor, feche-o"):
                builder.build(output_path)
