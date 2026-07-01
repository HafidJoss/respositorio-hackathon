import hashlib
import hmac
import secrets

from app.modules.auth.domain.ports import PasswordHasher

_ITERACIONES = 260_000
_ALGORITMO = "sha256"


class Pbkdf2PasswordHasher(PasswordHasher):
    """Hasher basado en hashlib.pbkdf2_hmac (stdlib) — sin dependencias externas.

    Formato persistido: "<salt_hex>$<hash_hex>".
    """

    def hashear(self, password: str) -> str:
        salt = secrets.token_hex(16)
        derivado = hashlib.pbkdf2_hmac(
            _ALGORITMO, password.encode("utf-8"), bytes.fromhex(salt), _ITERACIONES
        )
        return f"{salt}${derivado.hex()}"

    def verificar(self, password: str, password_hash: str) -> bool:
        try:
            salt, hash_esperado = password_hash.split("$", 1)
        except ValueError:
            return False
        derivado = hashlib.pbkdf2_hmac(
            _ALGORITMO, password.encode("utf-8"), bytes.fromhex(salt), _ITERACIONES
        )
        return hmac.compare_digest(derivado.hex(), hash_esperado)
