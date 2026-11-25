"""Gera o hash de uma senha para uso em .streamlit/secrets.toml.

Uso (na raiz do projeto):
    python scripts/gerar_hash_senha.py

Cole o resultado no secrets.toml:
    [usuarios]
    maria = "pbkdf2_sha256$260000$...$..."
"""

import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from codigo.autenticacao import gerar_hash_senha  # noqa: E402


def main():
    senha = getpass.getpass("Senha: ")
    confirmacao = getpass.getpass("Confirme a senha: ")
    if senha != confirmacao:
        sys.exit("As senhas não conferem.")
    if not senha:
        sys.exit("A senha não pode ser vazia.")
    print(gerar_hash_senha(senha))


if __name__ == "__main__":
    main()
