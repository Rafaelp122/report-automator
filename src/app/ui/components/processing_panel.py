from PySide6.QtWidgets import QFrame, QVBoxLayout, QProgressBar, QPushButton, QWidget
from PySide6.QtCore import Qt, Signal, Slot
from src.app.ui.components.log_view import LogView

class ProcessingPanel(QFrame):
    """
    Painel central que encapsula a lógica visual de processamento.
    """
    start_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainCard")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 25)
        layout.setSpacing(10)

        # Log View
        self.log_console = LogView(initial_text="Sistema pronto para operação.")
        layout.addWidget(self.log_console)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Action Button
        self.btn_action = QPushButton("GERAR RELATÓRIO MENSAL")
        self.btn_action.setObjectName("ActionButton")
        self.btn_action.setCursor(Qt.PointingHandCursor)
        self.btn_action.clicked.connect(self.start_requested.emit)
        layout.addWidget(self.btn_action)

    def set_busy(self, busy: bool):
        """Alterna o estado da UI entre processando e ocioso"""
        self.btn_action.setEnabled(not busy)
        if busy:
            self.progress_bar.setRange(0, 0) # Modo indeterminado
        else:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)

    def set_progress_success(self):
        """Define progresso como 100% no sucesso"""
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

    def log(self, message: str):
        """Encaminha o log para o console interno"""
        self.log_console.log(message)

    def clear_log(self):
        """Limpa o console de log"""
        self.log_console.clear()
