from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from core.database import SessionLocal
from services.auth_service import AuthService
from models.schemas import LoginSchema

class LoginView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.auth_service = AuthService(SessionLocal())
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("SaaS Locadora ERP")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px;")
        
        self.login_btn = QPushButton("Entrar")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        
        self.email_input.setFixedWidth(300)
        self.password_input.setFixedWidth(300)
        self.login_btn.setFixedWidth(300)

        layout.addWidget(title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        senha = self.password_input.text()
        
        try:
            user = self.auth_service.login(LoginSchema(email=email, senha=senha))
            QMessageBox.information(self, "Sucesso", f"Bem-vindo, {user.nome}!")
            self.main_window.go_to_dashboard()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erro Fatal", "Ocorreu um erro ao conectar no banco local.")
