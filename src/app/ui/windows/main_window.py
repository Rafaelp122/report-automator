from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Slot

from src.app.ui.workers.processor_worker import ProcessorWorker
from src.app.ui.components.header import Header
from src.app.ui.components.log_view import LogView

class MainWindow(QMainWindow):
    """
    Main Window Refatorada:
    - Composição de Componentes (Header, LogView).
    - Lógica de Layout mínima.
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Report Automator v1.0")
        self.setFixedSize(600, 560)
        self._load_styles()
        
        # Central Widget & Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # UI Components
        self.header = Header("Report Automator")
        self.main_layout.addWidget(self.header)

        # Card Principal (Contêiner)
        self._setup_main_card()
        
        # Footer
        self._setup_footer()

    def _load_styles(self):
        """Carrega o arquivo QSS de estilo"""
        try:
            with open("src/app/ui/styles/main.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Erro ao carregar estilos: {e}")

    def _setup_main_card(self):
        # Card Container (Margens externas)
        card_container = QWidget()
        card_layout_outer = QVBoxLayout(card_container)
        card_layout_outer.setContentsMargins(20, 20, 20, 20)

        # O Card Branco em si
        self.card_frame = QFrame()
        self.card_frame.setObjectName("MainCard")
        card_layout_inner = QVBoxLayout(self.card_frame)
        card_layout_inner.setContentsMargins(25, 20, 25, 25)
        card_layout_inner.setSpacing(10)

        # --- Componentes Internos do Card ---
        self.log_console = LogView(initial_text="Sistema pronto para operação.")
        card_layout_inner.addWidget(self.log_console)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        card_layout_inner.addWidget(self.progress_bar)

        self.btn_action = QPushButton("GERAR RELATÓRIO MENSAL")
        self.btn_action.setObjectName("ActionButton")
        self.btn_action.setCursor(Qt.PointingHandCursor)
        self.btn_action.clicked.connect(self.iniciar_processamento)
        card_layout_inner.addWidget(self.btn_action)

        card_layout_outer.addWidget(self.card_frame)
        self.main_layout.addWidget(card_container)

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
        """Setup do Worker e Thread"""
        self.btn_action.setEnabled(False)
        self.progress_bar.setRange(0, 0) # Indeterminate
        
        self.thread = QThread()
        self.worker = ProcessorWorker()
        self.worker.moveToThread(self.thread)
        
        # Conexão de Sinais via Componente LogView
        self.thread.started.connect(self.worker.run)
        self.worker.progress_log.connect(self.log_console.log)
        self.worker.finished.connect(self.finalizar_sucesso)
        self.worker.error.connect(self.finalizar_erro)
        
        # Cleanup
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()

    @Slot(str)
    def finalizar_sucesso(self, arquivo):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.btn_action.setEnabled(True)
        QMessageBox.information(self, "Sucesso", f"Relatório gerado com sucesso!\n{arquivo}")

    @Slot(str)
    def finalizar_erro(self, msg):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.btn_action.setEnabled(True)
        QMessageBox.critical(self, "Erro", f"Falha no processamento:\n{msg}")
