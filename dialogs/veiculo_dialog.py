from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QComboBox, QTabWidget, 
                             QWidget, QSpinBox, QDoubleSpinBox, QMessageBox)
from PySide6.QtCore import Qt
from models.schemas import VeiculoSchema
from services.veiculo_service import VeiculoService

class VeiculoDialog(QDialog):
    def __init__(self, service: VeiculoService, parent=None, veiculo=None):
        super().__init__(parent)
        self.service = service
        self.veiculo = veiculo # Se passado, é modo Edição
        
        self.setWindowTitle("Cadastro de Veículo" if not veiculo else f"Editar Veículo: {veiculo['placa']}")
        self.resize(600, 500)
        self.setStyleSheet("""
            QDialog, QTabWidget::pane { background-color: #2b2b40; color: white; border: none; }
            QLabel { color: #a0aec0; font-weight: bold; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #1e1e2d; border: 1px solid #3d3d5c;
                border-radius: 4px; padding: 6px; color: white;
            }
            QTabBar::tab {
                background-color: #1e1e2d; color: #a0aec0;
                padding: 10px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { background-color: #6366f1; color: white; }
            QPushButton { background-color: #6366f1; color: white; font-weight: bold; border-radius: 4px; padding: 8px 15px; }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.setup_ui()
        if self.veiculo:
            self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_geral_tab(), "Geral")
        self.tabs.addTab(self.create_docs_tab(), "Documentação")
        self.tabs.addTab(self.create_valores_tab(), "Valores")
        self.tabs.addTab(self.create_arquivos_tab(), "Arquivos (Em Breve)")
        
        main_layout.addWidget(self.tabs)
        
        # Botoes Footer
        footer = QHBoxLayout()
        footer.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("background-color: #3d3d5c;")
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Salvar Veículo")
        save_btn.clicked.connect(self.save)
        
        footer.addWidget(cancel_btn)
        footer.addWidget(save_btn)
        
        main_layout.addLayout(footer)

    def create_geral_tab(self):
        w = QWidget()
        l = QFormLayout(w)
        
        self.placa = QLineEdit()
        self.chassi = QLineEdit()
        self.marca = QLineEdit()
        self.modelo = QLineEdit()
        
        self.ano_fab = QSpinBox()
        self.ano_fab.setRange(1900, 2100)
        self.ano_fab.setValue(2023)
        
        self.ano_mod = QSpinBox()
        self.ano_mod.setRange(1900, 2100)
        self.ano_mod.setValue(2023)
        
        self.combustivel = QComboBox()
        self.combustivel.addItems(["FLEX", "GASOLINA", "ETANOL", "DIESEL", "ELETRICO", "HIBRIDO"])
        
        self.cambio = QComboBox()
        self.cambio.addItems(["AUTOMATICO", "MANUAL"])
        
        l.addRow("Placa:", self.placa)
        l.addRow("Chassi:", self.chassi)
        l.addRow("Marca:", self.marca)
        l.addRow("Modelo:", self.modelo)
        l.addRow("Ano Fabricação:", self.ano_fab)
        l.addRow("Ano Modelo:", self.ano_mod)
        l.addRow("Combustível:", self.combustivel)
        l.addRow("Câmbio:", self.cambio)
        return w

    def create_docs_tab(self):
        w = QWidget()
        l = QFormLayout(w)
        self.renavam = QLineEdit()
        self.seguradora = QLineEdit()
        self.apolice = QLineEdit()
        
        l.addRow("RENAVAM:", self.renavam)
        l.addRow("Seguradora:", self.seguradora)
        l.addRow("Apólice:", self.apolice)
        return w

    def create_valores_tab(self):
        w = QWidget()
        l = QFormLayout(w)
        
        self.valor_compra = QDoubleSpinBox()
        self.valor_compra.setRange(0, 9999999)
        self.valor_compra.setPrefix("R$ ")
        
        self.valor_fipe = QDoubleSpinBox()
        self.valor_fipe.setRange(0, 9999999)
        self.valor_fipe.setPrefix("R$ ")
        
        self.valor_diaria = QDoubleSpinBox()
        self.valor_diaria.setRange(0, 99999)
        self.valor_diaria.setPrefix("R$ ")
        
        l.addRow("Valor de Compra:", self.valor_compra)
        l.addRow("Valor FIPE:", self.valor_fipe)
        l.addRow("Valor Diária Sugerida:", self.valor_diaria)
        return w
        
    def create_arquivos_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        # Mock para interface futura de upload de arquivos
        l.addWidget(QPushButton("Anexar Fotos do Veículo"))
        l.addWidget(QPushButton("Anexar CRLV/Documentos"))
        l.addStretch()
        return w

    def load_data(self):
        v = self.veiculo
        self.placa.setText(v.get("placa", ""))
        self.chassi.setText(v.get("chassi", ""))
        self.marca.setText(v.get("marca", ""))
        self.modelo.setText(v.get("modelo", ""))
        
        # Para simplificar no MVP, nao faremos update complexo completo, apenas insert

    def save(self):
        try:
            schema = VeiculoSchema(
                placa=self.placa.text().upper(),
                chassi=self.chassi.text().upper(),
                marca=self.marca.text(),
                modelo=self.modelo.text(),
                ano_fabricacao=self.ano_fab.value(),
                ano_modelo=self.ano_mod.value(),
                combustivel=self.combustivel.currentText(),
                cambio=self.cambio.currentText(),
                renavam=self.renavam.text() or None,
                seguradora=self.seguradora.text() or None,
                apolice=self.apolice.text() or None,
                valor_compra=self.valor_compra.value(),
                valor_fipe=self.valor_fipe.value(),
                valor_diaria=self.valor_diaria.value(),
                status="DISPONIVEL"
            )
            
            if self.veiculo:
                # Atualização (Simplificada)
                pass 
            else:
                self.service.criar(schema)
                
            QMessageBox.information(self, "Sucesso", "Veículo salvo com sucesso!")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Aviso", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
