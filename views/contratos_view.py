from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QSplitter, QTableView, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from widgets.table_models import GenericTableModel
from dialogs.contrato_wizard import ContratoWizard
from dialogs.checkout_dialog import CheckoutDialog
from core.database import SessionLocal
from services.contrato_service import ContratoService

class ContratosView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = SessionLocal()
        self.service = ContratoService(self.db)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Toolbar Topo
        toolbar = QHBoxLayout()
        title_label = QLabel("Gestão de Contratos")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar placa, cliente, status...")
        self.search_input.setStyleSheet("""
            QLineEdit { background-color: #2b2b40; border: 1px solid #3d3d5c; border-radius: 4px; padding: 8px; color: white; }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        
        add_btn = QPushButton("Novo Contrato")
        add_btn.setStyleSheet("background-color: #6366f1; color: white; font-weight: bold; border-radius: 4px; padding: 8px 15px;")
        add_btn.clicked.connect(self.open_new_contrato)
        
        # Export button per user request via open questions
        export_btn = QPushButton("Exportar Excel/PDF")
        export_btn.setStyleSheet("background-color: #38a169; color: white; font-weight: bold; border-radius: 4px; padding: 8px 15px;")
        export_btn.clicked.connect(self.exportar_dados)
        
        toolbar.addWidget(title_label)
        toolbar.addStretch()
        toolbar.addWidget(self.search_input)
        toolbar.addWidget(export_btn)
        toolbar.addWidget(add_btn)
        
        layout.addLayout(toolbar)

        # Splitter Central
        self.splitter = QSplitter(Qt.Horizontal)
        
        self.table_view = QTableView()
        self.table_view.setStyleSheet("""
            QTableView { background-color: #2b2b40; color: white; gridline-color: #3d3d5c; border: 1px solid #3d3d5c; }
            QHeaderView::section { background-color: #1e1e2d; color: white; font-weight: bold; padding: 6px; border: 1px solid #3d3d5c; }
        """)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.clicked.connect(self.on_row_selected)
        
        self.headers = ["Status", "Veículo", "Data Fim", "Total R$"]
        self.keys = ["status", "veiculo_id", "data_fim_prevista", "valor_total"]
        self.base_model = GenericTableModel([], self.headers, self.keys, self)
        
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.base_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)
        
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        
        self.splitter.addWidget(self.table_view)

        # Painel Direito
        self.detail_panel = QWidget()
        self.detail_panel.setStyleSheet("background-color: #1e1e2d; border-radius: 8px; border: 1px solid #3d3d5c;")
        self.detail_layout = QVBoxLayout(self.detail_panel)
        
        self.lbl_detail = QLabel("Selecione um contrato")
        self.lbl_detail.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        
        self.btn_checkout = QPushButton("Realizar Check-Out")
        self.btn_checkout.setStyleSheet("background-color: #e53e3e; color: white; font-weight: bold; padding: 10px;")
        self.btn_checkout.setVisible(False)
        self.btn_checkout.clicked.connect(self.realizar_checkout)
        
        self.detail_layout.addWidget(self.lbl_detail)
        self.detail_layout.addStretch()
        self.detail_layout.addWidget(self.btn_checkout)
        
        self.splitter.addWidget(self.detail_panel)
        self.splitter.setSizes([700, 300])
        
        layout.addWidget(self.splitter)
        self.load_data()

    def load_data(self):
        contratos = self.service.listar_todos()
        data_dicts = [c.model_dump() for c in contratos]
        self.base_model.update_data(data_dicts)

    def filter_table(self, text):
        self.proxy_model.setFilterFixedString(text)

    def on_row_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        row = source_index.row()
        item = self.base_model.get_item(row)
        
        self.lbl_detail.setText(f"Contrato: {item['id'][:8]}\\nStatus: {item['status']}")
        
        if item['status'] == 'ATIVO':
            self.btn_checkout.setVisible(True)
            self.current_contrato_id = item['id']
        else:
            self.btn_checkout.setVisible(False)

    def open_new_contrato(self):
        wizard = ContratoWizard(self.service, self)
        if wizard.exec():
            self.load_data()
            
    def realizar_checkout(self):
        if not hasattr(self, 'current_contrato_id') or not self.current_contrato_id:
            return
            
        dlg = CheckoutDialog(self.service, self.current_contrato_id, self)
        if dlg.exec():
            self.load_data()
            self.main_window.dashboard_view.refresh_data()
            self.main_window.frota_view.load_data()
        
    def exportar_dados(self):
        QMessageBox.information(self, "Exportar", "As ferramentas de PDF/Excel através de utilitário compartilhado estão sendo implementadas.")
