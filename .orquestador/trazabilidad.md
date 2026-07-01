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

