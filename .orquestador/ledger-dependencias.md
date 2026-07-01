---
version: 1.0.0
estado: activo
dueño: compartido
---

# Ledger de dependencias cruzadas

> Cualquiera de los 3 roles añade una fila. Nadie borra ni edita
> una fila que no escribió — solo actualiza su columna Estado con
> nota de quién y cuándo.

| ID  | Descripción | Quién la necesita | Quién la resuelve | Estado | Bloqueo | Fecha |
| --- | ----------- | ----------------- | ----------------- | ------ | ------- | ----- |
| DEP-001 | fase-0 de `triaje` existe con nombre de archivo incorrecto (`fase-0/triaje.com` en vez de `fase-0/triaje.md`), aunque su contenido está completo y `congelada: true`. Tratado como válido por decisión explícita del dueño de sesión (Santiago) el 2026-07-01 — no bloquea Fase 1 de `triaje` | A | C | resuelto (pendiente solo renombrar el archivo) | local (triaje) | 2026-07-01 |
| DEP-002 | fase-0 de `bot-ivr-urgencias` no existe o no está congelada | A | C | pendiente | local (bot-ivr-urgencias) | 2026-07-01 |
| DEP-003 | fase-0 de `historial-clinico` no existe o no está congelada | A | C | pendiente | local (historial-clinico) | 2026-07-01 |
| DEP-004 | fase-0 de `notificaciones` no existe o no está congelada | A | C | pendiente | local (notificaciones) | 2026-07-01 |
| DEP-005 | fase-0 de `dashboard-enfermero` no existe o no está congelada | A | C | pendiente | local (dashboard-enfermero) | 2026-07-01 |
| DEP-006 | fase-0 de `dashboard-medico` no existe o no está congelada | A | C | pendiente — B construyó `PanelMedico.tsx` igual, por decisión explícita del dueño de sesión (Santiago) el 2026-07-01, priorizando MVP de hackathon. Sigue sin fase-0; C debe regularizar retroactivamente (ver `avance-frontend.md` y `trazabilidad.md`) | local (dashboard-medico) | 2026-07-01 |

## Regla de bloqueo local

Una dependencia pendiente detiene solo la pieza que la necesita —
nunca todo el trabajo del rol que espera. Si una fila permanece
`pendiente` por más de 3 sesiones, escalar a revisión directa entre
los 3 roles.

## Señal de alerta

Más de 3-4 filas abiertas simultáneas → Fase 0 del módulo no fue
lo bastante clara. La corrección es revisar Fase 0, no agregar más
supervisión continua.

