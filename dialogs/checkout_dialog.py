from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QDoubleSpinBox, QSpinBox, 
                             QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from datetime import datetime
from models.schemas import ContratoCheckoutSchema
from services.contrato_service import ContratoService

class CheckoutDialog(QDialog):
    def __init__(self, service: ContratoService, contrato_id: str, parent=None):
        super().__init__(parent)
        self.service = service
        self.contrato_id = contrato_id
        
        # Recupera contrato
        contrato_db = self.service.repo.get_by_id(contrato_id)
        if not contrato_db:
            raise ValueError("Contrato não encontrado.")
            
        self.contrato = contrato_db
        
        self.setWindowTitle(f"Check-Out Contrato {contrato_id[:8]}")
        self.resize(400, 450)
        
        self.setStyleSheet("""
            QDialog { background-color: #2b2b40; color: white; }
            QLabel { color: #a0aec0; font-weight: bold; }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #1e1e2d; border: 1px solid #3d3d5c;
                border-radius: 4px; padding: 6px; color: white;
            }
            QPushButton { background-color: #e53e3e; color: white; font-weight: bold; border-radius: 4px; padding: 10px; }
            QPushButton:hover { background-color: #c53030; }
        """)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        lbl_info = QLabel(f"Placa: {self.contrato.veiculo.placa} | KM Atual: {self.contrato.veiculo.quilometragem}")
        lbl_info.setStyleSheet("color: white; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(lbl_info)
        
        self.km_final = QSpinBox()
        self.km_final.setRange(self.contrato.km_inicial, 9999999)
        self.km_final.setValue(self.contrato.km_inicial)
        
        self.diarias_extras = QSpinBox()
        self.diarias_extras.setRange(0, 999)
        
        self.multas = QDoubleSpinBox()
        self.multas.setRange(0, 99999)
        self.multas.setPrefix("R$ ")
        
        self.avarias = QLineEdit()
        self.avarias.setPlaceholderText("Descreva caso haja avarias no check-out")
        
        form.addRow("KM Final:", self.km_final)
        form.addRow("Diárias Extras (Atraso):", self.diarias_extras)
        form.addRow("Multas/Taxas:", self.multas)
        form.addRow("Avarias:", self.avarias)
        
        layout.addLayout(form)
        
        btn_confirm = QPushButton("Confirmar Check-Out")
        btn_confirm.clicked.connect(self.process_checkout)
        layout.addStretch()
        layout.addWidget(btn_confirm)

    def process_checkout(self):
        try:
            schema = ContratoCheckoutSchema(
                km_final=self.km_final.value(),
                data_devolucao=datetime.now(),
                diarias_extras=self.diarias_extras.value(),
                multas_adicionais=self.multas.value(),
                avarias=self.avarias.text() or None,
            )
            
            self.service.encerrar_contrato(self.contrato_id, schema)
            
            QMessageBox.information(self, "Sucesso", "Check-Out realizado! O veículo já está DISPONÍVEL novamente.")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Aviso", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro no processamento: {str(e)}")
