from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class Footer(QWidget):
    """
    Componente visual para o rodapé da aplicação.
    Encapsula informações de versão e licença.
    """
    def __init__(self, version="v1.0.0", license_info="Licença MIT", parent=None):
        super().__init__(parent)
        self._setup_ui(version, license_info)

    def _setup_ui(self, version, license_info):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        
        self.label = QLabel(f"{version} | {license_info}")
        self.label.setObjectName("FooterLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.label)
