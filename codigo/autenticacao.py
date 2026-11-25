"""Verificação de credenciais (sem dependência do Streamlit).

As senhas em ``secrets.toml`` podem ser:
  * texto puro (compatível com a configuração anterior); ou
  * hash PBKDF2, no formato ``pbkdf2_sha256$iteracoes$sal$hash``, gerado por
    ``python scripts/gerar_hash_senha.py``.
"""

import hashlib
import hmac
import secrets
from collections.abc import Mapping

PREFIXO_HASH = "pbkdf2_sha256"
ITERACOES_PADRAO = 260_000


def gerar_hash_senha(
    senha: str,
    iteracoes: int = ITERACOES_PADRAO,
    sal: str | None = None,
) -> str:
    sal = sal or secrets.token_hex(16)
    derivada = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), sal.encode("utf-8"), iteracoes
    )
    return f"{PREFIXO_HASH}${iteracoes}${sal}${derivada.hex()}"


def _senha_confere(senha: str, armazenada: str) -> bool:
    if armazenada.startswith(f"{PREFIXO_HASH}$"):
        try:
            _, iteracoes, sal, hash_esperado = armazenada.split("$")
            derivada = hashlib.pbkdf2_hmac(
                "sha256", senha.encode("utf-8"), sal.encode("utf-8"), int(iteracoes)
            )
        except ValueError:
            return False
        return hmac.compare_digest(derivada.hex(), hash_esperado)

    return hmac.compare_digest(senha.encode("utf-8"), armazenada.encode("utf-8"))


def verificar_credenciais(
    usuario: str, senha: str, usuarios: Mapping[str, str]
) -> bool:
    if usuario not in usuarios:
        return False
    return _senha_confere(senha, str(usuarios[usuario]))
