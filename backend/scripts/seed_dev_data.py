"""Popula o banco de desenvolvimento com dados realistas e variados para testar
o sistema sem cadastro manual. Ver docs/10-SEED-DESENVOLVIMENTO.md.

Uso:
    python scripts/seed_dev_data.py [--reset] [--yes] [--com-uploads]

--reset       apaga (TRUNCATE) todas as tabelas da aplicação antes de semear.
              Sem essa flag, o script recusa rodar se já detectar dados de um
              seed anterior (idempotência simples).
--yes         pula a confirmação interativa do guard de ambiente (útil em
              scripts/CI, ex.: `docker exec`).
--com-uploads habilita upload real de fotos/assinaturas fictícias via o
              attachment_service (Supabase Storage) para um subconjunto de
              itens de checklist. Desabilitado por padrão — não arrisque
              sem confirmar que o bucket configurado no seu .env é de
              desenvolvimento, não o de produção.

O script recusa rodar contra qualquer banco cujo host não seja localhost,
127.0.0.1 ou "db" (serviço do docker-compose) — nunca roda contra produção.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal  # noqa: E402
from app.seed.guard import AmbienteInseguroError, garantir_ambiente_seguro  # noqa: E402
from app.seed.runner import resetar_banco, rodar_seed, usuario_seed_ja_existe  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reset", action="store_true", help="apaga os dados antes de semear")
    parser.add_argument("--yes", action="store_true", help="pula a confirmação interativa")
    parser.add_argument(
        "--com-uploads", action="store_true", help="habilita upload real de fotos fictícias"
    )
    args = parser.parse_args()

    try:
        garantir_ambiente_seguro(confirmar_automaticamente=args.yes)
    except AmbienteInseguroError as exc:
        print(f"\nAbortando: {exc}\n", file=sys.stderr)
        sys.exit(1)

    db = SessionLocal()
    try:
        if args.reset:
            resetar_banco(db)
        elif usuario_seed_ja_existe(db):
            print(
                "\nJá existem usuários de um seed anterior (e-mail @devseed.local). "
                "Rode com --reset para recriar a base do zero.\n",
                file=sys.stderr,
            )
            sys.exit(1)

        rodar_seed(db, com_uploads=args.com_uploads)
    finally:
        db.close()


if __name__ == "__main__":
    main()
