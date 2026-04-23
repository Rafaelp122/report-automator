import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.app.core.report_service import ReportService
from src.app.core.config_models import ReportConfig, ProjectConfig, FilesConfig

class TestReportService:
    @pytest.fixture
    def service(self):
        return ReportService()

    @pytest.fixture
    def base_config(self):
        return ReportConfig(
            projeto=ProjectConfig(mes=1, ano=2026),
            arquivos=FilesConfig(
                dados_origem='data_mock.xlsx',
                user_template='user.xlsx'
            )
        )

    @patch('src.app.core.report_service.Path')
    def test_generate_report_missing_origin(self, mock_path_cls, service, base_config):
        # Simula que o arquivo de origem não existe
        mock_path_cls.return_value.exists.return_value = False
        
        with pytest.raises(FileNotFoundError, match="Arquivo de origem não encontrado"):
            service.generate_report(base_config)

    @patch('src.app.core.report_service.Path')
    @patch('src.app.core.report_service.ReportBuilder')
    def test_use_user_template_when_exists(self, mock_builder_cls, mock_path_cls, service, base_config):
        # Simula que todos os arquivos existem
        mock_path_cls.return_value.exists.return_value = True
        mock_path_cls.return_value.__str__.return_value = 'user.xlsx'
        
        mock_builder = mock_builder_cls.return_value
        mock_builder.build.return_value = "output.xlsx"

        result = service.generate_report(base_config)

        # Verifica se o template_ativo foi definido como o do usuário
        assert base_config.arquivos.template_ativo == 'user.xlsx'
        assert result == "output.xlsx"

    @patch('src.app.core.report_service.Path')
    @patch('src.app.core.report_service.ReportBuilder')
    @patch('src.app.core.report_service.DEFAULT_TEMPLATE_PATH')
    def test_fallback_to_default_template(self, mock_default_tmpl, mock_builder_cls, mock_path_cls, service, base_config):
        # Simula que o de origem existe (primeira chamada do Path()), o do usuário NÃO (segunda chamada)
        # E o padrão SIM (mock_default_tmpl)
        
        # O mock_path_cls.return_value.exists será chamado para 'origem' e 'user_tmpl'
        # Vamos usar side_effect no exists do objeto retornado pelo Path()
        def exists_side_effect():
            # Primeira chamada (origem): True
            # Segunda chamada (user_tmpl): False
            yield True
            yield False
        
        mock_path_cls.return_value.exists.side_effect = exists_side_effect()
        mock_default_tmpl.exists.return_value = True
        mock_default_tmpl.__str__.return_value = 'template.xlsx'
        
        mock_builder = mock_builder_cls.return_value
        mock_builder.build.return_value = "output.xlsx"

        service.generate_report(base_config)

        # Verifica se houve o fallback para o template padrão
        assert base_config.arquivos.template_ativo == 'template.xlsx'

    @patch('src.app.core.report_service.Path')
    @patch('src.app.core.report_service.DEFAULT_TEMPLATE_PATH')
    def test_error_when_no_templates_exist(self, mock_default_tmpl, mock_path_cls, service, base_config):
        # Simula que apenas o arquivo de dados existe
        def exists_side_effect():
            yield True  # origem
            yield False # user_tmpl
        
        mock_path_cls.return_value.exists.side_effect = exists_side_effect()
        mock_default_tmpl.exists.return_value = False
        
        with pytest.raises(FileNotFoundError, match="Template padrão não encontrado"):
            service.generate_report(base_config)
