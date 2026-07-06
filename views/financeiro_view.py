from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QDialog, 
                             QFormLayout, QComboBox, QLineEdit, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from core.database import SessionLocal
from services.financeiro_service import FinanceiroService
from models.schemas import LancamentoSchema
from datetime import datetime

class LancamentoDialog(QDialog):
    def __init__(self, service: FinanceiroService, parent=None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle("Novo Lançamento Financeiro")
        self.resize(350, 400)
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
        self.tipo_box.addItems(["RECEITA", "DESPESA"])
        
        self.valor_input = QLineEdit()
        self.categoria_box = QComboBox()
        self.categoria_box.addItems(["ALUGUEL", "MANUTENCAO", "SALARIOS", "IMPOSTOS", "OUTROS"])
        
        self.desc_input = QLineEdit()
        
        layout.addRow("Tipo:", self.tipo_box)
        layout.addRow("Valor (R$):", self.valor_input)
        layout.addRow("Categoria:", self.categoria_box)
        layout.addRow("Descrição:", self.desc_input)
        
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.save_lancamento)
        layout.addRow(save_btn)

    def save_lancamento(self):
        try:
            val = float(self.valor_input.text())
            schema = LancamentoSchema(
                tipo=self.tipo_box.currentText(),
                valor=val,
                categoria=self.categoria_box.currentText(),
                descricao=self.desc_input.text(),
                status="PAGO",
                data_vencimento=datetime.now(),
                data_pagamento=datetime.now()
            )
            self.service.registrar_lancamento(schema)
            QMessageBox.information(self, "Sucesso", "Lançamento registrado com sucesso!")
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Validação", "Insira um valor numérico válido.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro: {str(e)}")


class FinanceiroView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = SessionLocal()
        self.service = FinanceiroService(self.db)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Fluxo de Caixa / Financeiro")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Barra de Ações
        actions_layout = QHBoxLayout()
        add_btn = QPushButton("Novo Lançamento")
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
        add_btn.clicked.connect(self.open_new_lancamento_dialog)
        actions_layout.addStretch()
        actions_layout.addWidget(add_btn)
        layout.addLayout(actions_layout)

        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tipo", "Descrição", "Categoria", "Valor", "Data"])
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
        # Para simplificar, listamos todos usando o repo base get_all
        lancamentos = self.service.repo.get_all()
        self.table.setRowCount(len(lancamentos))
        
        for row, lanc in enumerate(lancamentos):
            tipo_item = QTableWidgetItem(lanc.tipo)
            if lanc.tipo == "RECEITA":
                tipo_item.setForeground(QColor("#48bb78"))
            else:
                tipo_item.setForeground(QColor("#f56565"))
                
            self.table.setItem(row, 0, tipo_item)
            self.table.setItem(row, 1, QTableWidgetItem(lanc.descricao))
            self.table.setItem(row, 2, QTableWidgetItem(lanc.categoria))
            self.table.setItem(row, 3, QTableWidgetItem(f"R$ {lanc.valor:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(lanc.data_vencimento.strftime("%d/%m/%Y")))

    def open_new_lancamento_dialog(self):
        dialog = LancamentoDialog(self.service, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
            # Atualizar dashboard para recalcular métricas financeiras se estiver ativo
            self.main_window.dashboard_view.refresh_data()
