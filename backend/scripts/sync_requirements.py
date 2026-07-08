"""Gera requirements.txt a partir de pyproject.toml (fonte da verdade).

A Vercel instala dependencias do backend a partir de pyproject.toml (via uv);
o ambiente local usa requirements.txt (via pip). Rodar este script sempre que
uma dependencia for adicionada/alterada em pyproject.toml, para os dois
arquivos nao ficarem dessincronizados.

Uso:
    python scripts/sync_requirements.py [--check]

--check: nao escreve nada, só sai com código 1 se requirements.txt estiver
desatualizado em relação a pyproject.toml (útil em CI/pre-commit).
"""

import sys
import tomllib
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = BACKEND_DIR / "pyproject.toml"
REQUIREMENTS_PATH = BACKEND_DIR / "requirements.txt"


def gerar_conteudo_requirements() -> str:
    dados = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    principais = dados["project"]["dependencies"]
    dev = dados.get("dependency-groups", {}).get("dev", [])

    linhas = [*principais, "", *dev]
    return "\n".join(linhas) + "\n"


def main() -> None:
    conteudo_gerado = gerar_conteudo_requirements()
    conteudo_atual = (
        REQUIREMENTS_PATH.read_text(encoding="utf-8") if REQUIREMENTS_PATH.exists() else None
    )

    if "--check" in sys.argv:
        if conteudo_atual != conteudo_gerado:
            print("requirements.txt está desatualizado em relação a pyproject.toml.")
            print("Rode `python scripts/sync_requirements.py` para corrigir.")
            sys.exit(1)
        print("requirements.txt já está sincronizado com pyproject.toml.")
        return

    if conteudo_atual == conteudo_gerado:
        print("requirements.txt já está sincronizado com pyproject.toml.")
        return

    REQUIREMENTS_PATH.write_text(conteudo_gerado, encoding="utf-8")
    print(f"requirements.txt atualizado a partir de {PYPROJECT_PATH.name}.")


if __name__ == "__main__":
    main()
