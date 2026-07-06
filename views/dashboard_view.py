from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from core.database import SessionLocal
from services.dashboard_service import DashboardService

class DashboardView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = SessionLocal()
        self.service = DashboardService(self.db)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Título
        title_label = QLabel("Dashboard Geral")
        title_label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(title_label)

        # Grid de KPI Cards
        self.kpi_layout = QGridLayout()
        self.kpi_layout.setSpacing(15)
        self.main_layout.addLayout(self.kpi_layout)

        # Layout horizontal para os gráficos
        self.charts_layout = QHBoxLayout()
        self.charts_layout.setSpacing(20)
        self.main_layout.addLayout(self.charts_layout)

        self.refresh_data()

    def create_kpi_card(self, title, value, color_hex):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2b2b40;
                border: 1px solid #3d3d5c;
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #a0aec0; font-size: 13px; font-weight: bold;")
        
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet(f"color: {color_hex}; font-size: 22px; font-weight: bold;")

        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        return card

    def refresh_data(self):
        data = self.service.obter_resumo()

        # Limpar kpi_layout
        for i in reversed(range(self.kpi_layout.count())): 
            widget = self.kpi_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Adicionar novos KPI cards
        self.kpi_layout.addWidget(self.create_kpi_card("Receita do Mês", f"R$ {data['receitas_mes']:.2f}", "#48bb78"), 0, 0)
        self.kpi_layout.addWidget(self.create_kpi_card("Despesa do Mês", f"R$ {data['despesas_mes']:.2f}", "#f56565"), 0, 1)
        self.kpi_layout.addWidget(self.create_kpi_card("Lucro Líquido", f"R$ {data['lucro_mes']:.2f}", "#6366f1"), 0, 2)
        self.kpi_layout.addWidget(self.create_kpi_card("Veículos Alugados", f"{data['veiculos_alugados']} / {data['veiculos_totais']}", "#ecc94b"), 0, 3)

        # Limpar gráficos anteriores
        for i in reversed(range(self.charts_layout.count())):
            widget = self.charts_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Gráfico 1: Receita vs Despesa (Barras)
        fig1 = Figure(figsize=(5, 4), facecolor='#2b2b40')
        canvas1 = FigureCanvas(fig1)
        ax1 = fig1.add_subplot(111)
        ax1.set_facecolor('#2b2b40')
        ax1.bar(['Receitas', 'Despesas', 'Lucro'], [data['receitas_mes'], data['despesas_mes'], data['lucro_mes']], color=['#48bb78', '#f56565', '#6366f1'])
        ax1.tick_params(colors='white')
        ax1.spines['bottom'].set_color('#3d3d5c')
        ax1.spines['top'].set_color('#3d3d5c')
        ax1.spines['left'].set_color('#3d3d5c')
        ax1.spines['right'].set_color('#3d3d5c')
        ax1.set_title("Fluxo Financeiro Mensal", color='white', fontsize=12, pad=10)
        
        # Gráfico 2: Ocupação de Frota (Rosca / Pizza)
        fig2 = Figure(figsize=(5, 4), facecolor='#2b2b40')
        canvas2 = FigureCanvas(fig2)
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor('#2b2b40')
        
        labels = ['Disponíveis', 'Locados', 'Manutenção']
        sizes = [data['veiculos_disponiveis'], data['veiculos_alugados'], data['veiculos_manutencao']]
        colors = ['#38a169', '#ecc94b', '#e53e3e']
        
        # Filtrar apenas estados com valor > 0 para evitar erros de render
        non_zero = [(l, s, c) for l, s, c in zip(labels, sizes, colors) if s > 0]
        if non_zero:
            act_labels, act_sizes, act_colors = zip(*non_zero)
            ax2.pie(act_sizes, labels=act_labels, colors=act_colors, autopct='%1.1f%%', textprops={'color':"w"})
        else:
            ax2.text(0.5, 0.5, "Sem veículos cadastrados", color="white", ha="center")
            
        ax2.set_title("Ocupação da Frota", color='white', fontsize=12, pad=10)

        self.charts_layout.addWidget(canvas1)
        self.charts_layout.addWidget(canvas2)
