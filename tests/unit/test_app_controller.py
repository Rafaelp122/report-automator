import os
import shutil
import pytest
from unittest.mock import MagicMock, patch
from src.app.ui.controllers.app_controller import AppController

class TestAppController:
    @pytest.fixture
    def mock_view(self):
        view = MagicMock()
        view.processing_panel = MagicMock()
        view.processing_panel.input_origin = MagicMock()
        view.processing_panel.input_template = MagicMock()
        return view

    @pytest.fixture
    def mock_config_manager(self):
        cm = MagicMock()
        cm.load_config.return_value = {
            'arquivos': {
                'dados_origem': '',
                'user_template': ''
            },
            'mapeamento': {}
        }
        return cm

    def test_importar_arquivo_copies_file(self, tmp_path, mock_view, mock_config_manager):
        # Setup
        controller = AppController(mock_view, mock_config_manager)
        
        # Create a source file
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        source_file = source_dir / "test.xlsx"
        source_file.write_text("dummy content")
        
        # Mock project root for data/input
        with patch("os.path.join", side_effect=lambda *args: "/".join(args)):
            with patch("os.makedirs"):
                with patch("shutil.copy2") as mock_copy:
                    with patch("os.path.exists", return_value=False):
                        with patch("os.path.abspath", side_effect=lambda x: x):
                            new_path = controller._importar_arquivo(str(source_file))
                            
                            assert "data/input/test.xlsx" in new_path
                            mock_copy.assert_called_once()

    def test_atualizar_origem_automatica(self, mock_view, mock_config_manager):
        controller = AppController(mock_view, mock_config_manager)
        
        with patch.object(controller, '_importar_arquivo', return_value="data/input/new_test.xlsx"):
            controller.atualizar_origem_automatica("any/path/new_test.xlsx")
            
            assert controller.config['arquivos']['dados_origem'] == "data/input/new_test.xlsx"
            mock_view.processing_panel.input_origin.setText.assert_called_with("data/input/new_test.xlsx")
            mock_config_manager.save_config.assert_called()

    def test_atualizar_template_automatico(self, mock_view, mock_config_manager):
        controller = AppController(mock_view, mock_config_manager)
        
        with patch.object(controller, '_importar_arquivo', return_value="data/input/template.xlsx"):
            controller.atualizar_template_automatico("any/path/template.xlsx")
            
            assert controller.config['arquivos']['user_template'] == "data/input/template.xlsx"
            mock_view.processing_panel.input_template.setText.assert_called_with("data/input/template.xlsx")
            mock_config_manager.save_config.assert_called()
