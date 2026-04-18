from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PySide6.QtCore import Qt

class MappingTable(QWidget):
    """
    Componente que encapsula a tabela de mapeamento e seus controles (+/-).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        mapping_label = QLabel("Mapeamento (Aba Origem -> Célula Destino):")
        mapping_label.setObjectName("FieldLabel")
        layout.addWidget(mapping_label)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Aba na Origem", "Célula no Template"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedHeight(120)
        layout.addWidget(self.table)
        
        # Mapping Controls
        mapping_btns = QHBoxLayout()
        btn_add = QPushButton("+ Adicionar")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self.add_row)
        
        btn_remove = QPushButton("- Remover")
        btn_remove.setCursor(Qt.PointingHandCursor)
        btn_remove.clicked.connect(self.remove_last_row)
        
        mapping_btns.addWidget(btn_add)
        mapping_btns.addWidget(btn_remove)
        layout.addLayout(mapping_btns)

    def add_row(self, aba="", celula=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(aba))
        self.table.setItem(row, 1, QTableWidgetItem(celula))

    def remove_last_row(self):
        row_count = self.table.rowCount()
        if row_count > 0:
            self.table.removeRow(row_count - 1)

    def get_mapping(self):
        """Retorna o dicionário de mapeamento extraído da tabela"""
        mapeamento = {}
        for row in range(self.table.rowCount()):
            item_aba = self.table.item(row, 0)
            item_celula = self.table.item(row, 1)
            if item_aba and item_celula:
                aba = item_aba.text().strip()
                celula = item_celula.text().strip()
                if aba and celula:
                    mapeamento[aba] = celula
        return mapeamento

    def set_mapping(self, mapeamento):
        """Preenche a tabela com os dados fornecidos"""
        self.table.setRowCount(0)
        if mapeamento:
            for aba, celula in mapeamento.items():
                self.add_row(aba, celula)
