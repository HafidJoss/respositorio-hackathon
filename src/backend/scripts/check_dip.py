"""Verifica DIP: el dominio de un módulo nunca importa su infraestructura
(00-arquitectura-y-calidad.md §1) ni la infraestructura de otro módulo.

Uso: python scripts/check_dip.py --module registro_pacientes
"""

import argparse
import ast
import sys
from pathlib import Path

MODULES_ROOT = Path(__file__).resolve().parent.parent / "app" / "modules"


def _imports_de(archivo: Path) -> list[str]:
    arbol = ast.parse(archivo.read_text(), filename=str(archivo))
    nombres = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres.extend(alias.name for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            nombres.append(nodo.module)
    return nombres


def _viola_dip(modulo: str, importe: str) -> bool:
    prefijo_infra = f"app.modules.{modulo}.infrastructure"
    if importe.startswith(prefijo_infra):
        return True
    return any(
        importe.startswith(f"app.modules.{otro}.infrastructure")
        for otro in _listar_modulos()
        if otro != modulo
    )


def _listar_modulos() -> list[str]:
    return sorted(p.name for p in MODULES_ROOT.iterdir() if p.is_dir() and p.name != "__pycache__")


def verificar(modulo: str) -> list[str]:
    dominio = MODULES_ROOT / modulo / "domain"
    violaciones = []
    for archivo in dominio.rglob("*.py"):
        for importe in _imports_de(archivo):
            if _viola_dip(modulo, importe):
                violaciones.append(f"{archivo.relative_to(MODULES_ROOT.parent.parent)}: {importe}")
    return violaciones


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    args = parser.parse_args()

    violaciones = verificar(args.module)
    if violaciones:
        print(f"DIP violado en '{args.module}': 0 imports infra->domain esperado")
        for v in violaciones:
            print(f"  - {v}")
        return 1
    print(f"OK: 0 imports infra->domain en dominio de '{args.module}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
