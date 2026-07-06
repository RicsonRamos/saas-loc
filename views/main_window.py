import sys
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QWidget, 
                             QHBoxLayout, QVBoxLayout, QPushButton, QLabel)
from PySide6.QtCore import Qt
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.frota_view import FrotaView
from views.clientes_view import ClientesView
from views.contratos_view import ContratosView
from views.financeiro_view import FinanceiroView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SaaS Locadora - ERP Desktop")
        self.resize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2d;
            }
        """)

        # O widget central será um StackedWidget.
        # Ele conterá duas telas principais:
        # 1. Tela de Login (pura, sem sidebar)
        # 2. Tela Principal do Sistema (com sidebar + conteúdo móvel)
        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)

        # 1. Login View
        self.login_view = LoginView(self)
        self.root_stack.addWidget(self.login_view)

        # 2. Container Principal (Sidebar + Sub-telas)
        self.main_app_widget = QWidget()
        self.main_app_layout = QHBoxLayout(self.main_app_widget)
        self.main_app_layout.setContentsMargins(0, 0, 0, 0)
        self.main_app_layout.setSpacing(0)

        self.setup_sidebar()

        # Stack de conteúdo (Dashboard, Clientes, Financeiro)
        self.content_stack = QStackedWidget()
        self.main_app_layout.addWidget(self.content_stack)

        self.dashboard_view = DashboardView(self)
        self.frota_view = FrotaView(self)
        self.clientes_view = ClientesView(self)
        self.contratos_view = ContratosView(self)
        self.financeiro_view = FinanceiroView(self)

        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.addWidget(self.frota_view)
        self.content_stack.addWidget(self.clientes_view)
        self.content_stack.addWidget(self.contratos_view)
        self.content_stack.addWidget(self.financeiro_view)

        self.root_stack.addWidget(self.main_app_widget)

        # Começa no Login
        self.root_stack.setCurrentWidget(self.login_view)

    def setup_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #1a1a24;
                border-right: 1px solid #2b2b40;
            }
            QPushButton {
                background-color: transparent;
                color: #a0aec0;
                border: none;
                border-radius: 4px;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2b2b40;
                color: white;
            }
            QPushButton:checked {
                background-color: #6366f1;
                color: white;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)

        brand = QLabel("SaaS Locadora")
        brand.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 20px; padding-left: 10px;")
        layout.addWidget(brand)

        self.btn_dash = QPushButton("  Dashboard")
        self.btn_dash.setCheckable(True)
        self.btn_dash.setChecked(True)
        self.btn_dash.clicked.connect(lambda: self.switch_tab(0, self.btn_dash))
        layout.addWidget(self.btn_dash)

        self.btn_frota = QPushButton("  Frota")
        self.btn_frota.setCheckable(True)
        self.btn_frota.clicked.connect(lambda: self.switch_tab(1, self.btn_frota))
        layout.addWidget(self.btn_frota)

        self.btn_clientes = QPushButton("  Clientes")
        self.btn_clientes.setCheckable(True)
        self.btn_clientes.clicked.connect(lambda: self.switch_tab(2, self.btn_clientes))
        layout.addWidget(self.btn_clientes)
        
        self.btn_contratos = QPushButton("  Contratos")
        self.btn_contratos.setCheckable(True)
        self.btn_contratos.clicked.connect(lambda: self.switch_tab(3, self.btn_contratos))
        layout.addWidget(self.btn_contratos)

        self.btn_financeiro = QPushButton("  Financeiro")
        self.btn_financeiro.setCheckable(True)
        self.btn_financeiro.clicked.connect(lambda: self.switch_tab(4, self.btn_financeiro))
        layout.addWidget(self.btn_financeiro)

        layout.addStretch()

        btn_sair = QPushButton("  Sair")
        btn_sair.clicked.connect(self.logout)
        layout.addWidget(btn_sair)

        self.main_app_layout.addWidget(sidebar)

    def switch_tab(self, index, button):
        # Desmarcar todos os botões do menu
        self.btn_dash.setChecked(False)
        self.btn_frota.setChecked(False)
        self.btn_clientes.setChecked(False)
        self.btn_contratos.setChecked(False)
        self.btn_financeiro.setChecked(False)

        button.setChecked(True)
        self.content_stack.setCurrentIndex(index)

    def go_to_dashboard(self):
        # Transiciona para a tela principal
        self.root_stack.setCurrentWidget(self.main_app_widget)
        # Recarrega dados do dashboard
        self.dashboard_view.refresh_data()
        self.clientes_view.load_data()
        self.financeiro_view.load_data()

    def logout(self):
        self.root_stack.setCurrentWidget(self.login_view)
