"""Remove todas as pastas __pycache__ do projeto.

Uso (na raiz do projeto):
    python scripts/limpar_cache.py
"""

import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main():
    removidas = 0
    for pasta in RAIZ.rglob("__pycache__"):
        if "venv" in pasta.parts:
            continue
        shutil.rmtree(pasta, ignore_errors=True)
        removidas += 1
    print(f"{removidas} pasta(s) __pycache__ removida(s).")


if __name__ == "__main__":
    main()
