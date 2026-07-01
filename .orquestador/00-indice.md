---
version: 1.1.0
estado: activo
proyecto: Sistema de Gestión de Urgencias y Triaje — Posta Médica Rural
---

# Índice — .orquestador/

Punto de entrada obligatorio. Todo agente (C, A o B) lee este
archivo antes de tocar cualquier otro documento o código.

## Tabla de archivos vivos

| Archivo                        | Dueño             | Se toca cuando                            | Un agente de otro rol puede...                |
| ------------------------------ | ----------------- | ----------------------------------------- | --------------------------------------------- |
| `fase-0/{modulo}.md`           | C                 | Antes de habilitar Fase 1 de ese módulo   | Solo leer, nunca editar                       |
| `avance-backend.md`            | A                 | Durante construcción backend              | B solo lee, nunca edita                       |
| `avance-frontend.md`           | B                 | Durante construcción frontend             | A solo lee, nunca edita                       |
| `ledger-dependencias.md`       | Compartido        | Al aparecer un bloqueo cruzado real       | Cualquiera añade fila, nadie borra fila ajena |
| `trazabilidad.md`              | Compartido        | Al cerrar cualquier pieza                 | Cualquiera añade fila, nadie edita fila ajena |
| `contratos/openapi.json`       | A escribe · B lee | Tras cada cambio de endpoint              | B nunca edita a mano                          |
| `00-arquitectura-y-calidad.md` | C                 | Congelada — cambios requieren ADR-lite §5 | A y B leen, nunca editan                      |

## Módulos del proyecto — estado de Fase 0

| Módulo                | Fase 0       | Fase 1 backend | Fase 1 frontend |
| --------------------- | ------------ | -------------- | --------------- |
| `registro-pacientes`  | ✅ congelada | ⬜             | ⬜              |
| `triaje`              | ✅ congelada | ⬜             | ⬜              |
| `historial-clinico`   | ⬜ pendiente | ⬜             | ⬜              |
| `bot-ivr-urgencias`   | ⬜ pendiente | ⬜             | ⬜              |
| `dashboard-enfermero` | ⬜ pendiente | ⬜             | ⬜              |
| `dashboard-medico`    | ⬜ pendiente | ⬜             | ⬜              |
| `notificaciones`      | ⬜ pendiente | ⬜             | ⬜              |

**Orden de dependencia declarado (no arbitrario):** `registro-pacientes`
primero por ser la base del modelo `Usuario`/`Paciente`/`usuario_paciente`.
`triaje` segundo, por consumir directamente la búsqueda por DNI de
`registro-pacientes`. Los cinco módulos restantes no tienen orden
forzado entre sí, pero `bot-ivr-urgencias` y `dashboard-enfermero`
comparten el concepto de "nivel de atención" con `triaje` — revisar
ese fase-0 antes de fijar el glosario de los siguientes.

## Checklist de reentrada (agente retomando sesión interrumpida)

- [ ] ¿Qué módulo y qué rol tengo asignado esta sesión?
- [ ] ¿`fase-0/{modulo}.md` existe y está `congelada`? Si no → deten, escala a C
- [ ] ¿Mi archivo de avance tiene una tarea "en curso" sin cerrar de la sesión anterior?
- [ ] ¿Hay algo mío en `ledger-dependencias.md` esperando resolución de otro rol?
- [ ] `git status` — ¿algo fuera de mi alcance asignado aparece modificado? Si sí → deten, reporta, no commitees
- [ ] Solo entonces, continuar.

## Regla de alcance (heredada, sin excepción)

Ningún rol tiene dominio fijo permanente. Al inicio de cada sesión,
el alcance (módulo + rol) se declara explícito. Antes de cualquier
commit, se verifica que ningún archivo fuera de ese alcance quedó
modificado. Si aparece, el agente se detiene y reporta — no hace
stash, no descarta, no commitea por su cuenta.

