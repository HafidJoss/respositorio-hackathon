"""Valida contratos/openapi.json: sintaxis OpenAPI válida y sin drift
respecto al contrato esqueleto de un módulo (fase-0/{modulo}.md).

Uso: python scripts/validate_openapi.py --module registro_pacientes
"""

import argparse
import json
import sys
from pathlib import Path

from openapi_spec_validator import validate

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
OPENAPI_PATH = REPO_ROOT / "contratos" / "openapi.json"

ENDPOINTS_POR_MODULO = {
    "registro_pacientes": {
        ("post", "/usuarios"),
        ("get", "/usuarios/{usuario_id}"),
        ("post", "/pacientes"),
        ("get", "/pacientes"),
        ("post", "/usuarios/{usuario_id}/pacientes"),
        ("get", "/usuarios/{usuario_id}/pacientes"),
    },
    "triaje": {
        ("post", "/triajes"),
        ("get", "/triajes/{triaje_id}"),
        ("get", "/pacientes/{paciente_id}/triajes"),
        ("get", "/sintomas-comunes"),
    },
}


def _endpoints_reales(spec: dict) -> set[tuple[str, str]]:
    return {
        (metodo, ruta)
        for ruta, operaciones in spec["paths"].items()
        for metodo in operaciones
        if metodo in {"get", "post", "put", "patch", "delete"}
    }


def verificar(modulo: str) -> list[str]:
    spec = json.loads(OPENAPI_PATH.read_text())
    validate(spec)
    esperados = ENDPOINTS_POR_MODULO[modulo]
    reales = _endpoints_reales(spec)
    faltantes = esperados - reales
    return [f"falta en la app: {m.upper()} {r}" for m, r in faltantes]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True, choices=ENDPOINTS_POR_MODULO.keys())
    args = parser.parse_args()

    errores = verificar(args.module)
    if errores:
        print(f"Drift detectado en '{args.module}':")
        for e in errores:
            print(f"  - {e}")
        return 1
    print(f"OK: OpenAPI válido y sin drift para '{args.module}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
