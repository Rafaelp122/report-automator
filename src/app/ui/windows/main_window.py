from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Slot

from src.app.ui.workers.processor_worker import ProcessorWorker
from src.app.ui.components.header import Header
from src.app.ui.components.processing_panel import ProcessingPanel
from src.app.ui.utils.thread_manager import run_worker_thread

class MainWindow(QMainWindow):
    """
    Main Window Refatorada:
    - Atua como hospedeira de componentes especializados.
    - Delega burocracia de threads para o ThreadManager.
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Report Automator v1.0")
        self.setFixedSize(600, 560)
        self._load_styles()
        
        # Atributo para manter a thread viva (evitar Garbage Collection)
        self._active_thread = None
        
        # Central Widget & Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Header
        self.header = Header("Report Automator")
        self.main_layout.addWidget(self.header)

        # 2. Painel de Processamento (Encapsulado)
        self.processing_panel = ProcessingPanel()
        self.processing_panel.start_requested.connect(self.iniciar_processamento)
        
        # Container para margens do painel
        panel_container = QWidget()
        panel_layout = QVBoxLayout(panel_container)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.addWidget(self.processing_panel)
        self.main_layout.addWidget(panel_container)
        
        # 3. Footer
        self._setup_footer()

    def _load_styles(self):
        """Carrega o arquivo QSS de estilo"""
        try:
            with open("src/app/ui/styles/main.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Erro ao carregar estilos: {e}")

    def _setup_footer(self):
        footer_container = QWidget()
        footer_layout = QHBoxLayout(footer_container)
        
        self.footer_label = QLabel("v1.0.0 | Licença MIT")
        self.footer_label.setObjectName("FooterLabel")
        footer_layout.addStretch()
        footer_layout.addWidget(self.footer_label)
        footer_layout.addStretch()
        
        self.main_layout.addWidget(footer_container)

    def iniciar_processamento(self):
        """Delega o processamento pesado ao ThreadManager"""
        self.processing_panel.set_busy(True)
        
        # Instancia o Worker (Burocracia zero na MainWindow)
        worker = ProcessorWorker()
        
        # Executa via Gerenciador de Threads
        self._active_thread = run_worker_thread(
            worker,
            on_finished=self.finalizar_sucesso,
            on_error=self.finalizar_erro,
            on_log=self.processing_panel.log
        )

    @Slot(str)
    def finalizar_sucesso(self, arquivo):
        self.processing_panel.set_busy(False)
        self.processing_panel.set_progress_success()
        QMessageBox.information(self, "Sucesso", f"Relatório gerado com sucesso!\n{arquivo}")

    @Slot(str)
    def finalizar_erro(self, msg):
        self.processing_panel.set_busy(False)
        QMessageBox.critical(self, "Erro", f"Falha no processamento:\n{msg}")
