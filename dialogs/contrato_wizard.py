from PySide6.QtWidgets import (QWizard, QWizardPage, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QComboBox, QDoubleSpinBox, 
                             QDateEdit, QSpinBox, QMessageBox, QTableView, QHeaderView)
from PySide6.QtCore import Qt, QDate
from models.schemas import ContratoCreateSchema
from services.contrato_service import ContratoService
from widgets.table_models import GenericTableModel
from core.database import SessionLocal
from services.cliente_service import ClienteService
from services.veiculo_service import VeiculoService

class PageCliente(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Etapa 1: Selecionar Cliente")
        self.setSubTitle("Pesquise e selecione o cliente para o contrato.")
        
        self.layout = QVBoxLayout(self)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Pesquisar cliente (Nome ou CPF)...")
        self.layout.addWidget(self.search)
        
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        
        self.db = SessionLocal()
        self.service = ClienteService(self.db)
        
        self.model = GenericTableModel([], ["Nome", "Documento"], ["nome", "documento"])
        self.table.setModel(self.model)
        
        self.search.textChanged.connect(self.filter_clientes)
        self.load_data()
        
        self.registerField("cliente_id*", self.search) # Usando um hack temporario pra WizardField
        
        # Para salvar id real:
        self.selected_cliente_id = None
        self.table.clicked.connect(self.on_select)

    def load_data(self):
        clientes = [c.model_dump() for c in self.service.listar_todos() if c.ativo]
        self.model.update_data(clientes)

    def filter_clientes(self, text):
        # Filtro basico manual para nao gastar proxy proxy overhead no wizard agora
        all_clientes = [c.model_dump() for c in self.service.listar_todos() if c.ativo]
        filtered = [c for c in all_clientes if text.lower() in c['nome'].lower() or text in c['documento']]
        self.model.update_data(filtered)
        
    def on_select(self, index):
        item = self.model.get_item(index.row())
        self.selected_cliente_id = item['id']
        self.search.setText(item['nome']) # Aciona o registerField para validar
        
    def isComplete(self):
        return self.selected_cliente_id is not None

class PageVeiculo(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Etapa 2: Selecionar Veículo")
        self.setSubTitle("Apenas veículos com status DISPONÍVEL são exibidos.")
        
        self.layout = QVBoxLayout(self)
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        
        self.db = SessionLocal()
        self.service = VeiculoService(self.db)
        
        self.model = GenericTableModel([], ["Placa", "Modelo", "Diária"], ["placa", "modelo", "valor_diaria"])
        self.table.setModel(self.model)
        
        self.load_data()
        
        self.selected_veiculo_id = None
        self.valor_diaria_veiculo = 0.0
        self.km_inicial = 0
        self.table.clicked.connect(self.on_select)

    def load_data(self):
        veiculos = [v.model_dump() for v in self.service.listar_todos() if v.status == "DISPONIVEL"]
        self.model.update_data(veiculos)

    def on_select(self, index):
        item = self.model.get_item(index.row())
        self.selected_veiculo_id = item['id']
        self.valor_diaria_veiculo = item.get('valor_diaria', 0.0)
        self.km_inicial = item.get('quilometragem', 0)
        self.completeChanged.emit()

    def isComplete(self):
        return self.selected_veiculo_id is not None

class PageLocacao(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Etapa 3: Dados Financeiros e de Locação")
        
        self.layout = QFormLayout(self)
        
        self.data_inicio = QDateEdit(QDate.currentDate())
        self.data_fim = QDateEdit(QDate.currentDate().addDays(1))
        self.valor_diaria = QDoubleSpinBox()
        self.valor_diaria.setRange(0, 99999)
        self.desconto = QDoubleSpinBox()
        self.caucao = QDoubleSpinBox()
        self.caucao.setRange(0, 99999)
        
        self.forma_pag = QComboBox()
        self.forma_pag.addItems(["CARTAO", "PIX", "BOLETO", "DINHEIRO"])
        
        self.motorista = QLineEdit()
        
        self.layout.addRow("Data Início:", self.data_inicio)
        self.layout.addRow("Data Fim Prevista:", self.data_fim)
        self.layout.addRow("Valor Diária (R$):", self.valor_diaria)
        self.layout.addRow("Desconto (R$):", self.desconto)
        self.layout.addRow("Caução (R$):", self.caucao)
        self.layout.addRow("Pagamento:", self.forma_pag)
        self.layout.addRow("Motorista Adicional:", self.motorista)
        
    def initializePage(self):
        veiculo_page = self.wizard().page(1)
        self.valor_diaria.setValue(veiculo_page.valor_diaria_veiculo)

class ContratoWizard(QWizard):
    def __init__(self, service: ContratoService, parent=None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle("Novo Contrato de Locação")
        self.resize(700, 500)
        
        self.setStyleSheet("""
            QWizard { background-color: #2b2b40; color: white; }
            QLabel { color: white; }
            QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit {
                background-color: #1e1e2d; border: 1px solid #3d3d5c;
                border-radius: 4px; padding: 6px; color: white;
            }
        """)
        
        self.page1 = PageCliente()
        self.page2 = PageVeiculo()
        self.page3 = PageLocacao()
        
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.addPage(self.page3)
        # Check-list e Resumo podem ser estendidos depois.
        
    def accept(self):
        try:
            # Pegar dados de todas as pages
            p1 = self.page1
            p2 = self.page2
            p3 = self.page3
            
            dias = p3.data_inicio.date().daysTo(p3.data_fim.date())
            if dias < 1:
                raise ValueError("O contrato deve ter pelo menos 1 diária.")
                
            valor_total = (p3.valor_diaria.value() * dias) - p3.desconto.value()
            
            # Hora fixa provisoria
            dt_inicio = p3.data_inicio.dateTime().toPython()
            dt_fim = p3.data_fim.dateTime().toPython()
            
            schema = ContratoCreateSchema(
                cliente_id=p1.selected_cliente_id,
                veiculo_id=p2.selected_veiculo_id,
                data_inicio=dt_inicio,
                data_fim_prevista=dt_fim,
                valor_diaria=p3.valor_diaria.value(),
                valor_total=valor_total,
                desconto=p3.desconto.value(),
                caucao=p3.caucao.value(),
                forma_pagamento=p3.forma_pag.currentText(),
                km_inicial=p2.km_inicial,
                motorista_adicional=p3.motorista.text()
            )
            
            self.service.abrir_contrato(schema)
            QMessageBox.information(self, "Sucesso", "Contrato gerado com sucesso!")
            super().accept()
        except ValueError as e:
            QMessageBox.warning(self, "Aviso", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
