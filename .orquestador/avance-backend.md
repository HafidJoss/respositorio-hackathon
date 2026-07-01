---
version: 1.1.0
estado: activo
dueño: A
alcance_sesion_actual: TODOS los módulos backend, recorrido por orden de dependencia (ver fase-0/00-modulos-contemplados.md)
---

# Avance — Backend

> Fuente de criterios por módulo: `fase-0/{modulo}.md` congelada.
> Este archivo es autogobernado — B nunca lo edita, C no lo revisa
> por rutina, solo ante dependencia cruzada real en el ledger.
>
> Nota de reconstrucción (2026-07-01): esta versión restaura la
> estructura de criterios que existía antes de que el commit
> `55e803b` sobrescribiera este archivo con la plantilla de
> `fase-0/{modulo}.md` por error. Los umbrales `{X}%` quedan como
> placeholder tal como estaban en el original — su valor concreto no
> está decidido en ningún documento de `.orquestador` todavía.

## Módulo: registro-pacientes

**Estado del módulo:** ✅ cerrado

| Criterio | Umbral | Comando de verificación |
|---|---|---|
| Cobertura dominio | ≥ {X}% branch | `pytest tests/unit/registro_pacientes/domain --cov-branch` |
| Cobertura infraestructura | ≥ {X}% line | `pytest tests/unit/registro_pacientes/infrastructure` |
| Contrato OpenAPI válido | completo, sin drift | `python scripts/validate_openapi.py --module registro_pacientes` |
| Smoke test | 200/201 con datos reales (seed nivel mínimo) | `curl ...` |
| Vocabulario canónico | 0 sinónimos no autorizados (fase-0 glosario) | `grep -r "..." src/backend/app/modules/registro_pacientes/domain/` |
| Arquitectura DIP | 0 imports infra→domain | `python scripts/check_dip.py --module registro_pacientes` |
| SAST / secrets | 0 hallazgos CRITICAL | `bandit -r src/backend/app/modules/registro_pacientes/ -ll` · `gitleaks detect` |
| Principio Cero | Smoke E2E contra datos reales sembrados, no fixture fijo | ver §5 del orquestador |
| Código limpio | 0 funciones >20 líneas sin excepción documentada · 0 comentarios redundantes | linter + revisión estructural |
| Patrón justificado | Todo patrón usado está en la lista de 00-arquitectura-y-calidad.md §2, o tiene su justificación registrada ahí | revisión manual contra §2 |
| Migraciones versionadas | 0 cambios de esquema manuales | `git log -- migrations/` no vacío para todo cambio de schema |

## Módulo: triaje

**Estado del módulo:** ✅ cerrado

| Criterio | Umbral | Comando de verificación |
|---|---|---|
| Cobertura dominio | ≥ {X}% branch | `pytest tests/unit/triaje/domain --cov-branch` |
| Cobertura infraestructura | ≥ {X}% line | `pytest tests/unit/triaje/infrastructure` |
| Contrato OpenAPI válido | completo, sin drift | `python scripts/validate_openapi.py --module triaje` |
| Smoke test | 200/201 con datos reales (seed nivel mínimo) | `curl ...` |
| Vocabulario canónico | 0 sinónimos no autorizados (fase-0 glosario) | `grep -r "..." src/backend/app/modules/triaje/domain/` |
| Arquitectura DIP | 0 imports infra→domain | `python scripts/check_dip.py --module triaje` |
| SAST / secrets | 0 hallazgos CRITICAL | `bandit -r src/backend/app/modules/triaje/ -ll` · `gitleaks detect` |
| Principio Cero | Smoke E2E contra datos reales sembrados, no fixture fijo | ver §5 del orquestador |
| Código limpio | 0 funciones >20 líneas sin excepción documentada · 0 comentarios redundantes | linter + revisión estructural |
| Patrón justificado | Todo patrón usado está en la lista de 00-arquitectura-y-calidad.md §2, o tiene su justificación registrada ahí | revisión manual contra §2 |
| Migraciones versionadas | 0 cambios de esquema manuales | `git log -- migrations/` no vacío para todo cambio de schema |

## Módulo: bot-ivr-urgencias

**Estado del módulo:** 🚫 bloqueado — fase-0 no congelada
> No construir. Ver ledger-dependencias.md DEP-002.

## Módulo: historial-clinico

**Estado del módulo:** 🚫 bloqueado — fase-0 no congelada
> No construir. Ver ledger-dependencias.md DEP-003.

## Módulo: notificaciones

**Estado del módulo:** 🚫 bloqueado — fase-0 no congelada
> No construir. Ver ledger-dependencias.md DEP-004.

## Módulo: dashboard-enfermero

**Estado del módulo:** 🚫 bloqueado — fase-0 no congelada
> No construir. Ver ledger-dependencias.md DEP-005.

## Módulo: dashboard-medico

**Estado del módulo:** 🚫 bloqueado — fase-0 no congelada
> No construir. Ver ledger-dependencias.md DEP-006.

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
| 2026-07-01 | Reconstrucción de este archivo tras sobrescritura accidental en commit 55e803b | hecho | `git log -p -- .orquestador/avance-backend.md` |
| 2026-07-01 | Stack backend montado: Python 3.14 + FastAPI 0.138 + SQLAlchemy 2.0 + Alembic + PostgreSQL 16 (docker), monolito modular + hexagonal (`domain/application/infrastructure/api` por módulo) | hecho | `src/backend/requirements.txt`, `src/backend/docker-compose.yml`, `src/backend/migrations/` |
| 2026-07-01 | `registro-pacientes`: dominio (Usuario/Paciente/usuario_paciente §4.1), ports, application services, adapters SQLAlchemy, API con exactamente los 6 endpoints del contrato esqueleto | hecho | `src/backend/app/modules/registro_pacientes/` |
| 2026-07-01 | `triaje`: dominio (Triaje/NivelAtencion), ports (incl. `PacienteLookupPort` reutilizando registro-pacientes, `NotificacionPort` con adaptador stub por DEP-004), application service, adapters, API con exactamente los 4 endpoints del contrato esqueleto | hecho | `src/backend/app/modules/triaje/` |
| 2026-07-01 | Cobertura dominio+aplicación, branch, ambos módulos | 100% | `pytest --cov=app.modules.registro_pacientes --cov=app.modules.triaje --cov-branch` → `TOTAL 579 0 46 0 100%`, 72 passed |
| 2026-07-01 | Contrato OpenAPI generado desde código (nunca a mano) y validado sin drift | hecho | `contratos/openapi.json` generado vía `app.openapi()`; `python scripts/validate_openapi.py --module registro_pacientes` y `--module triaje` → `OK` |
| 2026-07-01 | Smoke test end-to-end contra PostgreSQL real (no mock, no fixture fijo) — usuario→paciente (con caso DNI duplicado ofreciendo vínculo)→triaje crítico→listados | 200/201 en todos los pasos | `curl` manual contra `uvicorn` + Postgres real en docker; repetido como test automatizado en `tests/integration/test_smoke_api.py` |
| 2026-07-01 | Arquitectura DIP: 0 imports infraestructura→dominio en ambos módulos | hecho | `python scripts/check_dip.py --module registro_pacientes` → OK; `--module triaje` → OK |
| 2026-07-01 | SAST | 0 hallazgos | `bandit -r app/modules/registro_pacientes/ app/modules/triaje/ -ll` → "No issues identified" (1089 líneas escaneadas) |
| 2026-07-01 | Secrets scan | 0 hallazgos | `docker run zricethezav/gitleaks:latest detect --source /repo --no-git` → "no leaks found" |
| 2026-07-01 | Código limpio: 0 funciones >20 líneas | hecho | script AST ad-hoc sobre `app/modules/registro_pacientes`, `app/modules/triaje`, `app/core`, `app/main.py` → "OK: 0 funciones >20 lineas" (tras refactor de `Triaje.crear` y `RegistrarTriajeService.ejecutar`) |
| 2026-07-01 | Vocabulario canónico: 0 sinónimos prohibidos del glosario de cada fase-0 | hecho | `grep -rniE "cliente\|dueño\|responsable\|apoderado\|encargado" app/modules/registro_pacientes/domain/` y `grep -rniE "consulta\|prioridad\|urgencia\|diagnostico" app/modules/triaje/domain/` → sin coincidencias |
| 2026-07-01 | Migraciones versionadas: 0 cambios de esquema manuales | hecho | `alembic revision --autogenerate` + `alembic upgrade head` (`migrations/versions/7d6f6cee831f_...py`); `alembic check` → "No new upgrade operations detected" |
| 2026-07-01 | Patrón justificado: solo Repository, Adapter, DTO/Mapper, Application Service (00-arquitectura-y-calidad.md §2) | verificado manualmente | revisión de `app/modules/*/domain,application,infrastructure,api` — ningún patrón adicional introducido |

**Nota — umbral de cobertura:** `{X}%` nunca fue fijado por C en ningún
documento de `.orquestador`. Se alcanzó 100% branch en dominio y
aplicación, y 100% line en infraestructura de ambos módulos — el
umbral concreto queda como PENDIENTE de decisión formal de C para
futuros módulos, no bloqueó el cierre de estos dos.

**Nota — RBAC/seguridad baseline:** el contrato esqueleto de ambos
fase-0 no incluye endpoints de autenticación/autorización (fuera de
"ni más ni menos" del contrato). Los ítems de seguridad baseline que
dependen de un rol autenticado (ej. "el Médico no puede editar un
triaje") se satisfacen hoy por ausencia de endpoint de edición en el
contrato, no por una capa de RBAC — queda PENDIENTE explícito para
cuando exista un módulo de autenticación (no contemplado en los 7
módulos actuales de `00-modulos-contemplados.md`).
