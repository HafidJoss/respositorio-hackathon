---
version: 1.1.0
estado: activo
dueño: B
alcance_sesion_actual: [declarar módulo + carpeta exacta al iniciar sesión]
---

# Avance — Frontend

> Fuente de criterios por módulo: `fase-0/{modulo}.md` congelada.
> Este archivo es autogobernado — A nunca lo edita, C no lo revisa
> por rutina, solo ante dependencia cruzada real en el ledger.
>
> **Corrección 2026-07-01:** esta versión anterior de este archivo
> contenía, por error de copia, el contenido íntegro de
> `avance-backend.md` (criterios de cobertura de dominio en Python,
> `bandit`, `check_dip.py`, etc. — no aplicables a frontend). Se
> reescribe aquí con criterios reales de frontend. No se fabrica
> historial retroactivo: las filas de "Log de avance" anteriores a
> hoy no existían.

## Criterios de código limpio (heredados de 00-arquitectura-y-calidad.md §3)

Aplican a todo módulo de frontend, sin repetirse por módulo:

- Funciones/componentes ≤ 20 líneas de lógica — excepción documentada si hay coordinación legítima
- Nombres significativos, vocabulario canónico del glosario de cada `fase-0/{modulo}.md`
- 0 comentarios redundantes o decorativos
- Componentes desacoplados de la capa de red (toda llamada HTTP pasa por `src/services/api.ts`, ninguna pantalla hace `fetch` directo)
- Manejo de errores estructurado — mensajes de `catch` se muestran al usuario, nunca solo `console.log`

## Módulo: registro-pacientes (frontend)

**Estado:** ✅ conectado a backend real — `RegistroPaciente.tsx` usa `POST /usuarios`,
`POST /pacientes`, `GET /pacientes`, `POST /usuarios/{id}/pacientes` vía `api.ts`.
Verificado E2E con Playwright contra backend real (usuario 201, paciente 201/vínculo).

## Módulo: triaje (frontend)

**Estado:** ✅ conectado a backend real — `NuevoTriaje.tsx` usa `POST /triajes` y
`GET /sintomas-comunes`. Refactorizado 2026-07-01 a formato de cuestionario clínico
(checkboxes reales para síntomas, radio buttons reales para nivel de atención,
manteniendo la paleta de colores crítico/moderado/leve ya definida). Verificado
E2E: el triaje enviado aparece de inmediato en `GET /pacientes/{id}/triajes`
(consumido por el Historial del Panel Médico).

## Módulo: auth (frontend) — fuera del índice de módulos de negocio original

**Estado:** ✅ conectado a backend real — `Login.tsx` usa `POST /auth/login` y
`POST /auth/registro` (módulo backend nuevo, ver `avance-backend.md`). El rol de
enrutamiento (`medico`/`enfermero`) viene del backend, no de la selección de UI.

## Módulo: dashboard-medico (frontend) — ⚠️ construido fuera de proceso

**Fase 0:** ⬜ no existe (`ledger-dependencias.md` DEP-006, sin resolver).
`00-arquitectura-y-calidad.md` §4 declara explícitamente que la estrategia de
sincronización de este dashboard "se resuelve en el fase-0... antes de que B
empiece esa pieza específica" — es decir, este módulo **no estaba autorizado**
a iniciarse bajo el proceso normal.

**Por qué existe código igual:** decisión explícita de Santiago (dueño de sesión)
el 2026-07-01, priorizando un MVP demostrable de hackathon sobre el orden de
fase-0. Documentado aquí para que C pueda auditar/regularizar retroactivamente,
no para aparentar que pasó por el proceso normal.

**Qué se construyó:** `PanelMedico.tsx` — cola de atención (dato mock, etiquetado
en UI como "datos de demostración"), vista de atención (modal) con enlace real a
"Ver Historial Clínico" (`GET /pacientes?dni=`, `GET /pacientes/{id}/triajes`),
checkbox "Marcar como Atendido" que mueve al paciente de la cola a la sección
"Mi Historial de Atenciones" — movimiento 100% en estado de React, instantáneo,
sin backend de alertas/vitales (no existe todavía).

**Qué falta para regularizar:** que C escriba `fase-0/dashboard-medico.md` y
congele el glosario/contrato; en ese momento este módulo se audita contra los
criterios reales (hoy no tiene fila de criterios porque no hay fase-0 de la que
derivarlos).

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
| ----- | ----- | ------ | --------- |
| 2026-07-01 | Login/registro conectados a `/auth/login` y `/auth/registro` reales | ✅ | E2E Playwright: 200/201 reales, cuentas médico/enfermero seedeadas |
| 2026-07-01 | `PanelMedico.tsx` construido (fuera de proceso, ver sección dedicada arriba) | ⚠️ funcional, sin fase-0 | Screenshots + E2E Playwright |
| 2026-07-01 | `NuevoTriaje.tsx` refactorizado a cuestionario clínico (checkboxes/radio reales) | ✅ | E2E Playwright: triaje 201, visible en historial real del paciente |
