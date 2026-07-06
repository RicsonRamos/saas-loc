import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow
import core.database as db
from loguru import logger

def setup_logs():
    logger.add("logs/app.log", rotation="1 MB", retention="10 days", compression="zip")

def main():
    setup_logs()
    logger.info("Iniciando SaaS Locadora ERP...")
    
    app = QApplication(sys.argv)
    
    # Configura fontes ou temas globais aqui se necessario
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
