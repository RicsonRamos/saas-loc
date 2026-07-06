import bcrypt
from core.database import SessionLocal
from models.usuario import Usuario

def create_default_admin():
    db = SessionLocal()
    admin = db.query(Usuario).filter(Usuario.email == "admin@admin.com").first()
    if not admin:
        hashed = bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        new_admin = Usuario(
            nome="Administrador",
            email="admin@admin.com",
            senha_hash=hashed,
            perfil="ADMIN"
        )
        db.add(new_admin)
        db.commit()
        print("Usuário Admin criado com sucesso. (email: admin@admin.com | senha: admin)")
    else:
        print("Usuário Admin já existe.")
    db.close()

if __name__ == "__main__":
    create_default_admin()
