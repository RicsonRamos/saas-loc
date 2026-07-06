from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel, 
                             QDialog, QFormLayout, QComboBox, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt
from core.database import SessionLocal
from services.cliente_service import ClienteService
from models.schemas import ClienteSchema

class ClienteDialog(QDialog):
    def __init__(self, service: ClienteService, parent=None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle("Novo Cliente")
        self.resize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b40;
                color: white;
            }
            QLabel {
                color: #a0aec0;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #1e1e2d;
                border: 1px solid #3d3d5c;
                border-radius: 4px;
                padding: 6px;
                color: white;
            }
            QPushButton {
                background-color: #6366f1;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        self.tipo_box = QComboBox()
        self.tipo_box.addItems(["FISICA", "JURIDICA"])
        
        self.nome_input = QLineEdit()
        self.doc_input = QLineEdit()
        self.cnh_input = QLineEdit()
        self.email_input = QLineEdit()
        self.tel_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.uf_input = QLineEdit()
        
        layout.addRow("Tipo:", self.tipo_box)
        layout.addRow("Nome/Razão Social:", self.nome_input)
        layout.addRow("CPF/CNPJ:", self.doc_input)
        layout.addRow("CNH:", self.cnh_input)
        layout.addRow("E-mail:", self.email_input)
        layout.addRow("Telefone:", self.tel_input)
        layout.addRow("Cidade:", self.cidade_input)
        layout.addRow("UF:", self.uf_input)
        
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.save_cliente)
        layout.addRow(save_btn)

    def save_cliente(self):
        try:
            # Prepara schema de dados com validações básicas
            schema = ClienteSchema(
                tipo_pessoa=self.tipo_box.currentText(),
                nome=self.nome_input.text(),
                documento=self.doc_input.text(),
                cnh=self.cnh_input.text() or None,
                email=self.email_input.text() or None,
                telefone=self.tel_input.text() or None,
                cidade=self.cidade_input.text() or None,
                uf=self.uf_input.text() or None
            )
            self.service.criar(schema)
            QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso!")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Validação", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")


class ClientesView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = SessionLocal()
        self.service = ClienteService(self.db)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Cadastro de Clientes")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Barra de Ações (Filtro e Botão de Adicionar)
        actions_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar por nome...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b40;
                border: 1px solid #3d3d5c;
                border-radius: 4px;
                padding: 8px;
                color: white;
            }
        """)
        self.search_input.textChanged.connect(self.filter_clientes)
        
        add_btn = QPushButton("Novo Cliente")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
        """)
        add_btn.clicked.connect(self.open_new_cliente_dialog)
        
        actions_layout.addWidget(self.search_input)
        actions_layout.addWidget(add_btn)
        layout.addLayout(actions_layout)

        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nome", "Tipo", "CPF/CNPJ", "E-mail", "Cidade", "Status"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b40;
                color: white;
                gridline-color: #3d3d5c;
                border: 1px solid #3d3d5c;
            }
            QHeaderView::section {
                background-color: #1e1e2d;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #3d3d5c;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        clientes = self.service.listar_todos()
        self.table.setRowCount(len(clientes))
        
        for row, cliente in enumerate(clientes):
            self.table.setItem(row, 0, QTableWidgetItem(cliente.nome))
            self.table.setItem(row, 1, QTableWidgetItem(cliente.tipo_pessoa))
            self.table.setItem(row, 2, QTableWidgetItem(cliente.documento))
            self.table.setItem(row, 3, QTableWidgetItem(cliente.email or "-"))
            self.table.setItem(row, 4, QTableWidgetItem(cliente.cidade or "-"))
            status = "Ativo" if cliente.ativo else "Inativo"
            self.table.setItem(row, 5, QTableWidgetItem(status))

    def filter_clientes(self):
        text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                self.table.setRowHidden(row, text not in item.text().lower())

    def open_new_cliente_dialog(self):
        dialog = ClienteDialog(self.service, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
