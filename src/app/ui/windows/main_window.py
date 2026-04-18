from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel

from src.app.ui.components.header import Header
from src.app.ui.components.processing_panel import ProcessingPanel
from src.app.ui.components.footer import Footer
from src.app.core.logger import logger

class MainWindow(QMainWindow):
    """
    Main Window Refatorada (View):
    Responsável apenas pelo layout e instanciação de componentes visuais.
    """
    
    def __init__(self):
        super().__init__()
        logger.info("Inicializando visual da MainWindow...")
        
        self.setWindowTitle("Report Automator v1.0")
        self.setMinimumSize(800, 800)
        self._load_styles()
        
        # UI Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header
        self.header = Header("Report Automator")
        self.main_layout.addWidget(self.header)

        # Painel de Processamento
        self.processing_panel = ProcessingPanel()
        
        panel_container = QWidget()
        panel_layout = QVBoxLayout(panel_container)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.addWidget(self.processing_panel)
        self.main_layout.addWidget(panel_container)
        
        # Footer
        self.footer = Footer(version="v1.0.0", license_info="Licença MIT")
        self.main_layout.addWidget(self.footer)
        
        logger.info("Visual da MainWindow pronto.")

    def _load_styles(self):
        try:
            with open("src/app/ui/styles/main.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Falha ao carregar estilos: {e}")
