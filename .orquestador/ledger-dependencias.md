---
version: 0.1.0
estado: activo
dueño: compartido
---
# Ledger de dependencias cruzadas

> Cualquiera de los 3 roles añade una fila. Nadie borra ni edita
> una fila que no escribió — solo actualiza su columna Estado con
> nota de quién y cuándo.

| ID | Descripción | Quién la necesita | Quién la resuelve | Estado | Bloqueo | Fecha |
|---|---|---|---|---|---|---|
| DEP-001 | [...] | A / B / C | A / B / C | pendiente / resuelta / excluida | local (pieza específica) | [fecha] |

## Regla de bloqueo local
Una dependencia pendiente detiene solo la pieza que la necesita —
nunca todo el trabajo del rol que espera. Si una fila permanece
`pendiente` por más de {N días/sesiones}, escalar a revisión
directa entre los 3 roles.

## Señal de alerta
Más de 3-4 filas abiertas simultáneas → Fase 0 del módulo no fue
lo bastante clara. La corrección es revisar Fase 0, no agregar más
supervisión continua.