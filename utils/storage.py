import os
import shutil
import uuid
from datetime import datetime

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "uploads")

def setup_storage():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def save_file(source_path: str, category: str = "geral") -> str:
    """
    Copia um arquivo do sistema para a pasta de uploads local e retorna o caminho relativo.
    """
    setup_storage()
    
    category_dir = os.path.join(UPLOAD_DIR, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)
        
    ext = os.path.splitext(source_path)[1]
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}{ext}"
    dest_path = os.path.join(category_dir, filename)
    
    shutil.copy2(source_path, dest_path)
    
    # Retorna path relativo para salvar no BD: "assets/uploads/categoria/nome.ext"
    return os.path.join("assets", "uploads", category, filename).replace("\\", "/")

def get_absolute_path(relative_path: str) -> str:
    if not relative_path:
        return ""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, relative_path)
