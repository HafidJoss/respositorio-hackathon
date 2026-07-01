---
version: 0.1.0
estado: activo
dueño: A
alcance_sesion_actual: [módulo + carpeta exacta]
---
# Avance — Backend

> Fuente de criterios por módulo: `fase-0/{modulo}.md` congelada.
> Este archivo es autogobernado — B nunca lo edita, C no lo revisa
> por rutina, solo ante dependencia cruzada real en el ledger.

## Módulo: {nombre}

| Criterio | Umbral | Comando de verificación |
|---|---|---|
| Cobertura dominio | ≥ {X}% branch | `pytest tests/unit/{modulo}/domain --cov-branch` |
| Cobertura infraestructura | ≥ {X}% line | `pytest tests/unit/{modulo}/infrastructure` |
| Contrato OpenAPI válido | completo, sin drift | `python scripts/validate_openapi.py --module {modulo}` |
| Smoke test | 200/201 con datos reales (seed nivel mínimo) | `curl ...` |
| Vocabulario canónico | 0 sinónimos no autorizados (fase-0 glosario) | `grep -r "..." src/{modulo}/domain/` |
| Arquitectura DIP | 0 imports infra→domain | `python scripts/check_dip.py --module {modulo}` |
| SAST / secrets | 0 hallazgos CRITICAL | `bandit -r src/{modulo}/ -ll` · `gitleaks detect` |
| Principio Cero | Smoke E2E contra datos reales sembrados, no fixture fijo | ver §5 del orquestador |
| Código limpio | 0 funciones >20 líneas sin excepción documentada · 0 comentarios redundantes | linter + revisión estructural |
| Patrón justificado | Todo patrón usado está en la lista de 00-arquitectura-y-calidad.md §2, o tiene su justificación registrada ahí | revisión manual contra §2 |
| Migraciones versionadas | 0 cambios de esquema manuales | `git log --  migrations/` no vacío para todo cambio de schema |

**Estado del módulo:** ⬜ pendiente / 🔵 en progreso / ✅ cerrado

## Regla de corrección automática
Intento 1 → analizar + corregir → re-ejecutar
Intento 2 → estrategia alternativa → re-ejecutar
Intento 3 → documentar estado exacto → detención
Tras 3 intentos → DETENCIÓN, espera instrucción humana

## Formato de detención
MÓDULO: {módulo}
CRITERIO FALLIDO: {criterio exacto}
VALOR OBTENIDO: {...}
VALOR ESPERADO: {...}
INTENTOS: {1|2|3}
QUÉ NECESITA EL HUMANO: {...}
SIGUIENTE PASO: {...}

## No regresión
Antes de cerrar módulo N, verificar que módulos 1..N-1 siguen en
verde en un solo run. Regresión bloquea avance — no se salta.

## Log de avance
| Fecha | Tarea | Estado | Evidencia |
|---|---|---|---|