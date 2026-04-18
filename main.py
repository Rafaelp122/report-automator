import sys
from PySide6.QtWidgets import QApplication
from src.app.ui.windows.main_window import MainWindow
from src.app.ui.controllers.app_controller import AppController
from src.app.infra.config_manager import ConfigManager
from src.app.core.logger import setup_logger

def main():
    # Inicializa o logging globalmente
    setup_logger()
    
    app = QApplication(sys.argv)
    
    # Injeção de Dependências
    config_manager = ConfigManager()
    window = MainWindow()
    
    # O Controller orquestra a janela e o gerenciador de configurações
    controller = AppController(window, config_manager)
    
    window.show()
    
    # Inicia a lógica inicial (validação) após exibir a janela
    controller.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
