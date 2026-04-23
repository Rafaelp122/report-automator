import pytest
from unittest.mock import MagicMock
from src.app.ui.workers.processor_worker import ProcessorWorker
from src.app.core.config_models import ReportConfig, FilesConfig
from src.app.core.report_service import ReportService

class TestProcessorWorker:
    
    def test_run_success(self, qtbot, tmp_path):
        dados_path = tmp_path / "dados.xlsx"
        dados_path.touch()
        
        config = ReportConfig(
            arquivos=FilesConfig(
                dados_origem=str(dados_path)
            )
        )
        
        mock_service = MagicMock(spec=ReportService)
        mock_service.generate_report.return_value = "resultado.xlsx"
        
        worker = ProcessorWorker(config, mock_service)
        
        with qtbot.waitSignal(worker.finished, timeout=2000) as blocker:
            worker.run()
                
        assert blocker.args == ["resultado.xlsx"]
        mock_service.generate_report.assert_called_once()

    def test_run_service_error(self, qtbot):
        config = ReportConfig()
        mock_service = MagicMock(spec=ReportService)
        mock_service.generate_report.side_effect = Exception("Erro genérico")
        
        worker = ProcessorWorker(config, mock_service)
        with qtbot.waitSignal(worker.error, timeout=2000) as blocker:
            worker.run()
        
        assert "Erro genérico" in blocker.args[0]

    def test_run_data_file_missing_in_service(self, qtbot):
        config = ReportConfig(
            arquivos=FilesConfig(dados_origem='missing_data.xlsx')
        )
        # Usamos o serviço real aqui para testar a integração se desejado, 
        # mas como é teste unitário do worker, mockamos o serviço para lançar o erro esperado
        mock_service = MagicMock(spec=ReportService)
        mock_service.generate_report.side_effect = FileNotFoundError("Arquivo de origem não encontrado")
        
        worker = ProcessorWorker(config, mock_service)
        
        with qtbot.waitSignal(worker.error, timeout=2000) as blocker:
            worker.run()
            
        assert "Arquivo de origem não encontrado" in blocker.args[0]
