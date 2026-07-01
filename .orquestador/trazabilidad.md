---
version: 1.1.0
estado: activo
dueño: compartido
---

# Trazabilidad — punto de fusión único

> Única tabla donde se cruzan los 3 trabajos. Nadie necesita leer
> el archivo de avance de otro rol — solo esta fila.

| ID negocio (fase-0) | Backend (A) | Frontend (B) | Dependencia (si aplica) | Estado | Evidencia |
| ------------------- | ----------- | ------------ | ----------------------- | ------ | --------- |
| registro-pacientes | ✅ cerrado | ✅ conectado | Ninguna — base del dominio | completo E2E | `avance-backend.md` 2026-07-01: cobertura/DIP/bandit/OpenAPI OK. `avance-frontend.md` 2026-07-01: `RegistroPaciente.tsx` contra backend real, smoke E2E Playwright (200/201 reales) |
| triaje | ✅ cerrado | ✅ conectado | registro-pacientes (búsqueda por DNI, reutilizada vía `PacienteLookupPort`) | completo E2E | `avance-backend.md` 2026-07-01: cobertura/DIP/bandit/OpenAPI OK. `avance-frontend.md` 2026-07-01: `NuevoTriaje.tsx` refactorizado a cuestionario clínico, triaje 201 visible de inmediato en historial real |

## Módulos sin fase-0 (fuera del índice de negocio original)

> Estas filas no cumplen el formato de la tabla anterior porque no
> tienen `fase-0/{modulo}.md` congelada. Se documentan aparte para no
> aparentar que pasaron por el proceso normal — ver `ledger-dependencias.md`.

| Módulo | Backend (A) | Frontend (B) | Estado | Evidencia |
| ------ | ----------- | ------------- | ------ | --------- |
| auth (login/roles de personal) | ✅ nuevo módulo, sin fase-0 propia | ✅ conectado | funcional, pendiente de que C lo regularice con fase-0 | `avance-backend.md`/`avance-frontend.md` 2026-07-01: `POST /auth/login`, `POST /auth/registro` reales, E2E Playwright con cuentas médico/enfermero seedeadas |
| dashboard-medico | — (no requiere backend propio aún) | ⚠️ construido fuera de proceso | funcional en demo, bloqueado formalmente por DEP-006 | `avance-frontend.md` 2026-07-01: `PanelMedico.tsx` — cola/alertas mock etiquetadas como demo, "Ver Historial Clínico" y envío de triaje 100% reales, decisión explícita de Santiago documentada |

## Regla de integridad numérica

Ningún número (cobertura, conteo de tests, endpoints) se escribe
aquí sin haber ejecutado el comando que lo produce en ese mismo
momento — nunca por copia de una sección anterior ni por inferencia
aritmética. Si un número no coincide con uno anterior del mismo
documento, se reporta la discrepancia explícitamente, nunca se
sobreescribe en silencio.

## Cierre del sistema completo

```
☐ avance-backend.md — todos los módulos en verde, sin regresión
☐ avance-frontend.md — todas las piezas en verde, sin regresión
☐ ledger-dependencias.md — cada fila resuelta o explícitamente excluida
☐ Principio Cero verificado en smoke E2E final contra datos reales
```

