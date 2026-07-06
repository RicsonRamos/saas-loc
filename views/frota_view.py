from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QSplitter, QTableView, QHeaderView)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from widgets.table_models import GenericTableModel
from dialogs.veiculo_dialog import VeiculoDialog
from core.database import SessionLocal
from services.veiculo_service import VeiculoService

class FrotaView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = SessionLocal()
        self.service = VeiculoService(self.db)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Toolbar Topo
        toolbar = QHBoxLayout()
        title_label = QLabel("Gestão de Frota")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar placa, modelo, marca...")
        self.search_input.setStyleSheet("""
            QLineEdit { background-color: #2b2b40; border: 1px solid #3d3d5c; border-radius: 4px; padding: 8px; color: white; }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        
        add_btn = QPushButton("Novo Veículo")
        add_btn.setStyleSheet("background-color: #6366f1; color: white; font-weight: bold; border-radius: 4px; padding: 8px 15px;")
        add_btn.clicked.connect(self.open_new_veiculo)
        
        toolbar.addWidget(title_label)
        toolbar.addStretch()
        toolbar.addWidget(self.search_input)
        toolbar.addWidget(add_btn)
        
        layout.addLayout(toolbar)

        # Splitter Central
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Lado Esquerdo: Tabela (QTableView)
        self.table_view = QTableView()
        self.table_view.setStyleSheet("""
            QTableView { background-color: #2b2b40; color: white; gridline-color: #3d3d5c; border: 1px solid #3d3d5c; }
            QHeaderView::section { background-color: #1e1e2d; color: white; font-weight: bold; padding: 6px; border: 1px solid #3d3d5c; }
        """)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.clicked.connect(self.on_row_selected)
        
        # Configurar Model da Tabela
        self.headers = ["Placa", "Marca", "Modelo", "Ano", "Status", "Diária"]
        self.keys = ["placa", "marca", "modelo", "ano_modelo", "status", "valor_diaria"]
        self.base_model = GenericTableModel([], self.headers, self.keys, self)
        
        # Adicionar Proxy para filtro inteligente e ordenação
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.base_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1) # Filtra em todas as colunas
        
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        
        self.splitter.addWidget(self.table_view)

        # Lado Direito: Painel de Detalhes
        self.detail_panel = QWidget()
        self.detail_panel.setStyleSheet("background-color: #1e1e2d; border-radius: 8px; border: 1px solid #3d3d5c;")
        self.detail_layout = QVBoxLayout(self.detail_panel)
        self.detail_layout.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_detail_placa = QLabel("Selecione um veículo")
        self.lbl_detail_placa.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        
        self.lbl_detail_status = QLabel("-")
        self.lbl_detail_status.setStyleSheet("color: #a0aec0;")
        
        self.detail_layout.addWidget(self.lbl_detail_placa)
        self.detail_layout.addWidget(self.lbl_detail_status)
        self.detail_layout.addStretch()
        
        self.splitter.addWidget(self.detail_panel)
        
        # Definir tamanhos iniciais do splitter (70% tabela, 30% painel)
        self.splitter.setSizes([700, 300])
        
        layout.addWidget(self.splitter)
        self.load_data()

    def load_data(self):
        veiculos_schemas = self.service.listar_todos()
        data_dicts = [v.model_dump() for v in veiculos_schemas]
        self.base_model.update_data(data_dicts)

    def filter_table(self, text):
        self.proxy_model.setFilterFixedString(text)

    def on_row_selected(self, index):
        # Mapeia index do proxy para o modelo base
        source_index = self.proxy_model.mapToSource(index)
        row = source_index.row()
        item = self.base_model.get_item(row)
        
        self.lbl_detail_placa.setText(f"{item.get('marca')} {item.get('modelo')} ({item.get('placa')})")
        self.lbl_detail_status.setText(f"Status: {item.get('status')} | Diária: R$ {item.get('valor_diaria', 0):.2f}")

    def open_new_veiculo(self):
        dlg = VeiculoDialog(self.service, self)
        if dlg.exec():
            self.load_data()
            self.main_window.dashboard_view.refresh_data()
