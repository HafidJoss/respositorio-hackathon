`---
version: 1.0.0
estado: activo
dueño: compartido

---

# Trazabilidad — punto de fusión único

> Única tabla donde se cruzan los 3 trabajos. Nadie necesita leer
> el archivo de avance de otro rol — solo esta fila.

| ID negocio (fase-0) | Backend (A) | Frontend (B) | Dependencia (si aplica) | Estado | Evidencia |
| ------------------- | ----------- | ------------ | ----------------------- | ------ | --------- |
| registro-pacientes | ✅ cerrado | ⬜ pendiente | Ninguna — base del dominio | parcial (backend listo, falta frontend) | `avance-backend.md` Log de avance 2026-07-01: 100% cobertura branch, DIP OK, bandit/gitleaks OK, OpenAPI sin drift, smoke E2E contra PostgreSQL real |
| triaje | ✅ cerrado | ⬜ pendiente | registro-pacientes (búsqueda por DNI, reutilizada vía `PacienteLookupPort`) | parcial (backend listo, falta frontend) | `avance-backend.md` Log de avance 2026-07-01: 100% cobertura branch, DIP OK, bandit/gitleaks OK, OpenAPI sin drift, smoke E2E contra PostgreSQL real |

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

